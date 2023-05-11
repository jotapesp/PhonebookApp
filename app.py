import sqlite3
from app.functions import *
from manage import *
import sys

class Menu:
    def __init__(self):
        self.options = [['Quit', None]]
    def addOption(self, name, function):
        self.options.append([name, function])
    def show(self):
        print("\nMenu")
        print("----")
        for i, option in enumerate(self.options):
            print(f"[{i}] - {option[0]}")
        print()
    def execute(self):
        while True:
            self.show()
            option = validate_integer_range('Choose an option: ', 0,
                                            len(self.options) - 1)
            if option == 0:
                break
            # print(self.options[option][1])
            self.options[option][1]()

class AppContacts:
    @staticmethod
    def ask_info(info):
        return input(f"{info}: ")
    @staticmethod
    def show_data(data):
        print(f"Name: {data.name}")
        for telephone in data.telephone_list:
            print(f"Telephone: {telephone}")
        print()
    @staticmethod
    def show_data_telephone(data):
        print(f"Name: {data.name}")
        for i, telephone in enumerate(data.telephone_list):
            print(f"{i} - Telephone: {telephone}")
        print()
    def __init__(self, database):
        self.manager = DBManager(database)
        self.menu = Menu()
        self.menu.addOption('New', self.new)
        self.menu.addOption('Edit', self.edit)
        self.menu.addOption('Delete', self.delete)
        self.menu.addOption('List', self.list)
        self.last_db_name = None
    def ask_telephone_type(self, default=None):
        for i, type in enumerate(self.manager.telephone_types_list):
            print(f"{i} - {type} ", end=None)
        t = validate_integer_range("Type: ", 0,
                            len(self.manager.telephone_types_list) - 1, default)
        return self.manager.telephone_types_list[t]
    def search(self, name):
        if isinstance(name, str):
            name = Name(name)
        data = self.manager.searchName(name)
        return data
    def new(self):
        new = AppContacts.ask_info("Name")
        if null_or_blank(new):
            return
        name = Name(new)
        if self.search(name) is not None:
            print("Name already exists!")
            return
        entry = Contact(name)
        self.menu_telephones(entry)
        self.manager.new(entry)
    def delete(self):
        name = AppContacts.ask_info("Name")
        if null_or_blank(name):
            return
        p = self.search(name)
        if p is not None:
            self.manager.delete(p)
        else:
            print("No match.")
    def edit(self):
        name = AppContacts.ask_info("Name")
        if null_or_blank(name):
            return
        p = self.search(name)
        if p is not None:
            AppContacts.show_data(p)
            print("In case you do not want to edit name info, hit 'ENTER'/'Return'")
            new = AppContacts.ask_info("Name")
            if not null_or_blank(new):
                p.name = new
            self.menu_telephones(p)
            self.manager.update(p)
        else:
            print("No match!")
    def menu_telephones(self, data):
        while True:
            print("\nEditing telephone info\n")
            AppContacts.show_data_telephone(data)
            if len(data.telephone_list) > 0:
                print("\n[E] - edit\n[D] - delete\n", end="")
            print("[N] - new\n[Q] - quit\n")
            operation = input("Choose an operation: ")
            operation = operation.lower()
            if operation not in ["e", "d", "n", "q"]:
                print("Invalid operation. Enter E, D, N or Q")
                continue
            if operation == 'e' and len(dados.telephone_list) > 0:
                self.edit_telephones(data)
            elif operation == 'd' and len(dados.telephone_list) > 0:
                self.delete_telephone(data)
            elif operation == 'n':
                self.new_telephone(data)
            elif operation == 'q':
                break
    def new_telephone(self, data):
        telephone = AppContacts.ask_info("Telephone: ")
        if null_or_blank(telephone):
            return
        if data.searchTelephone(telephone) is not None:
            print("Telephone number already exists!")
        type = self.ask_telephone_type()
        data.telephone_list.addItem(Telephone(telephone, type))
    def delete_telephone(self, data):
        ind = validate_integer_range_or_blank("Enter the number equivalent to the telephone to delete. Enter/Return to quit.",
                                            0, len(data.telephone_list) - 1)
        if ind is None:
            return
        data.telephone_list.remove(data.telephone_list[ind])
    def edit_telephones(self, data):
        ind = validate_integer_range_or_blank("Enter the number equivalent to the telephone to delete. Enter/Return to quit.",
                                            0, len(data.telephone_list) - 1)
        if ind is None:
            return
        telephone = data.telephone_list[ind]
        print(f"Telephone: {telephone}")
        new_tel = AppContacts.ask_info("New telephone or Enter/Return to cancel: ")
        if not null_or_blank(new_tel):
            telephone.number = new_tel
        print("Enter the number equivalent to the new telephone type or Enter/Return to cancel type editing")
        telephone.type = self.ask_telephone_type(
                default=self.manager.telephone_types_list.searchItem[telephone.type])
    def list(self):
        print("\nContact List")
        print("-" * 60)
        for data in self.manager.list():
            # print(data.name)
            # print(data.name.id)
            # print(data)
            AppContacts.show_data(data)
            print()
        print("-" * 60)
    def execute(self):
        self.menu.execute()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = AppContacts(sys.argv[1])
        app.execute()
    else:
        print("Error: database name should be given.")
        print("Usage: app.py database_name")
