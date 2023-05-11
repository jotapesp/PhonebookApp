from functools import total_ordering

class UniqueList:
    def __init__(self, elem_class):
        self.list = []
        self.elem_class = elem_class
    def __len__(self):
        return len(self.list)
    def __iter__(self):
        return iter(self.list)
    def __getitem__(self, p):
        return self.list[p]
    def validIndex(self, index):
        return index >= 0 and index <= len(self.list)
    def addItem(self, elem):
        if self.searchItem(elem) == -1:
            self.list.append(elem)
    def removeItem(self, elem):
        self.list.remove(elem)
    def searchItem(self, elem):
        self.verify_item(elem)
        try:
            return self.list.index(elem)
        except ValueError:
            return -1
    def verify_item(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError("Invalid type")
    def sort(self, key=None):
        self.list.sort(key=key)

class UniqueListDB(UniqueList):
    def __init__(self, elem_class):
        super().__init__(elem_class)
        self.deleted = []
    def removeItem(self, elem):
        if elem.id is not None:
            self.deleted.append(elem.id)
        super().removeItem(elem)
    def clear_deleted(self):
        self.deleted = []

@total_ordering
class Name:
    def __init__(self, name, id_=None):
        self.name = name
        self.id = id_
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"<Class {type(self).__name__} at 0x{id(self):x} Name: {self.__name} Key: {self.__key}>"
    def __eq__(self, other):
        return self.name == other.name
    def __lt__(self, other):
        return self.name < other.name
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if value is None or not value.strip():
            raise ValueError("Name can't be blank or None.")
        self.__name = value
        self.__key = Name.createKey(value)
    @property
    def key(self):
        return self.__key
    @staticmethod
    def createKey(value):
        return value.strip().lower()

@total_ordering
class TelephoneType:
    def __init__(self, id_, type):
        self.type = type
        self.id = id_
    def __str__(self):
        return f"({self.type})"
    def __eq__(self, other):
        if other is None:
            return False
        return self.type == other.type
    def __lt__(self, other):
        return self.type < other.type

class Telephone:
    def __init__(self, number, type=None, id_=None, id_name=None):
        self.number = number
        self.type = type
        self.id = id_
        self.id_name = id_name
    def __str__(self):
        if self.type is not None:
            type = self.type
        else:
            type = ''
        return f"{self.number} {type}"
    def __eq__(self, other):
        return self.number == other.number and (self.type == other.type or
        (self.type is None or other.type is None))
    @property
    def number(self):
        return self.__number
    @number.setter
    def number(self, value):
        if value is None or not value.strip():
            raise ValueError("Number can't be blank or None.")
        self.__number = value

class TelephoneTypes(UniqueList):
    def __init__(self):
        super().__init__(TelephoneType)

class TelephoneList(UniqueListDB):
    def __init__(self):
        super().__init__(Telephone)

class Contact:
    def __init__(self, name):
        self.name = name
        self.telephone_list = TelephoneList()
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if not isinstance(value, Name):
            raise TypeError("Name should be an instance of Name class")
        self.__name = value
    def searchTelephone(self, telephone):
        pos = self.telephone_list.searchItem(Telephone(telephone))
        if pos == -1:
            return None
        else:
            return self.telephone_list[pos]
