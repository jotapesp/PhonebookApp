import sqlite3
from contextlib import closing
import os
from classes.db_classes import *

DB = """
    CREATE TABLE names(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        name text);
    CREATE TABLE telephones(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        number text,
                        id_name integer,
                        id_type integer);
    CREATE TABLE types(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        description text);
    INSERT INTO types(description) VALUES ('Mobile');
    INSERT INTO types(description) VALUES ('Home');
    INSERT INTO types(description) VALUES ('Fax');
    INSERT INTO types(description) VALUES ('Work');
    """

class DBManager:
    def __init__(self, database):
        self.database = database
        self.telephone_types_list = TelephoneTypes()
        database_path = os.path.join('database/', database)
        new = not os.path.exists(database_path)
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
        if new:
            self.create_database()
        self.load_types()
    def create_database(self):
        self.conn.executescript(DB)
    def load_types(self):
        for type in self.conn.execute("SELECT * FROM types").fetchall():
            id_ = type['id']
            description = type['description']
            self.telephone_types_list.addItem(TelephoneType(id_, description))
    def searchName(self, name):
        if not isinstance(name, Name):
            raise TypeError("Name should be an instance of Name class")
        found = self.conn.execute("""SELECT count(*) FROM names WHERE
                                    name = ?""", (name.name,)).fetchone()
        if found[0] > 0:
            return self.load_using_name(name)
        else:
            return None
    def load_using_id(self, name):
        if not isinstance(name, Name):
            raise TypeError("Name should be an instance of Name class")
        match = self.conn.execute("SELECT * FROM names WHERE id = ?", (name.id,))
        return self.load(match.fetchone())
    def load_using_name(self, name):
        match = self.conn.execute("SELECT * FROM names WHERE name = ?", (name.name,))
        return self.load(match.fetchone())
    def load(self, match):
        # print(match)
        if match is None:
            return None
        # print(match["name"])
        # print(match["id"])
        new = Contact(Name(match["name"], match["id"]))
        for telephone in self.conn.execute("""SELECT * FROM telephones
                                            WHERE id_name = ?""", (new.name.id,)):
            telephone_number = Telephone(telephone['number'], type=None,
                                        id_=telephone['id'], id_name=telephone['id_name'])
            for type in self.telephone_types_list:
                if type.id == telephone['id_type']:
                    telephone_number.type = type
                    break
            new.telephone_list.addItem(telephone_number)
        return new
    def list(self):
        match = self.conn.execute("SELECT * FROM names ORDER BY name")
        # print(match)
        for entry in match:
            # print(entry)
            yield self.load(entry)
    def new(self, entry):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO names(name) VALUES (?)",
                        (str(entry.name),))
            entry.name.id = cur.lastrowid
            for telephone in entry.telephone_list:
                cur.execute("""INSERT INTO telephones(number, id_name, id_type)
                                VALUES (?, ?, ?)""", (telephone.number,
                                entry.name.id, telephone.type.id))
                telephone.id = cur.lastrowid
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()
    def update(self, entry):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE names SET name = ? WHERE id = ?",
                        (str(entry.name), entry.name.id))
            for telephone in entry.telephone_list:
                if telephone.id == None:
                    cur.execute("""INSERT INTO telephones(number, id_name, id_type)
                                VALUES (?, ?, ?)""", (telephone.number, entry.name.id,
                                                    telephone.type.id))
                    telephone.id = cur.lastrowid
                else:
                    cur.execute("""UPDATE telephones SET number = ?, id_name = ?,
                                id_type = ? WHERE id = ?""", (telephone.number,
                                                            entry.name.id,
                                                            telephone.type.id,
                                                            telephone.id))
            for deleted_entry in entry.telephone_list.deleted:
                cur.execute("DELETE FROM TELEPHONES WHERE id = ?", (deleted_entry,))
            self.conn.commit()
            entry.telephone_list.clear_deleted()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()
    def delete(self, entry):
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM telephones WHERE id_name = ?", (entry.name.id,))
            cur.execute("DELETE FROM names WHERE id = ?", (entry.name.id,))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()
