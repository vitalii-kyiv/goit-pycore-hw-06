from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pattern = r'^\d{10}$'
    def __init__(self, value):
        if re.match(self.pattern, value):
            super().__init__(value)
        else:
            raise ValueError("Wrong number format, number should contain 10 digits")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone (self, phone):
        phone = Phone(phone)
        self.phones.append(phone)
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:  
                self.phones.remove(p)
                return
        raise ValueError("Phone not found in the record")
        
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:  
            if p.value == old_phone:  
                p.value = new_phone 
                return  
        raise ValueError("Phone not found in the record")  
            
        
    def find_phone(self, phone):
        for p in self.phones:  
            if p.value == phone:  
                return  p.value
        raise ValueError("Phone not found in the record")  


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name '{name}' not found")
        

def parse_input(user_input):
    if not user_input.strip():  
        return "", []  
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "There is no contact with this name."
        except IndexError:
            return "Give me name."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        return "This name already in contacts"
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    name = args[0]  
    return f"{name}: {contacts[name]}"


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "":
            print("You didn't enter any command. Please try again.")
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "show":
            print(show_phone(args, contacts))
        elif command == "all":
            print("Contacts:")
            for name, phone in contacts.items():
                print(f"{name}: {phone}")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()