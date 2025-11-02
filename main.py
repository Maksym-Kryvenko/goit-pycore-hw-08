from collections import UserDict
from functools import wraps
import re
import datetime
import pickle

class Field:
    """
    Base class for fields in a contact record.
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Class for contact name with validation.
    """
    def __init__(self, name):
        super().__init__(Name.__validate_name(name))
    
    @staticmethod
    def __validate_name(name: str) -> str:
        """
        Validate the name to contain only letters and spaces.
        :param name: str The input name.

        Return: Cleaned name if valid, raise an error otherwise.
        """
        clean_name = name.strip().replace("  "," ")
        if clean_name.isalpha():
            clean_name = re.findall(r"[A-Za-zА-Яа-яЁёЇїІіЄєҐґ\s]+", clean_name)
            if isinstance(clean_name, list) and clean_name:
                clean_name = clean_name[0]
            if clean_name:
                return clean_name
        raise ValueError("Invalid name format. Name should contain only letters and spaces")
    

class Phone(Field):
    """
    Class for contact phone number with validation.
    """
    def __init__(self, number: str):
        super().__init__(Phone.__normalize_phone(number))
    
    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value

    @staticmethod
    def __normalize_phone(phone_number: str) -> str:
        """
        Normalize a phone number to the format +380XXXXXXXXX.
        :param phone_number: str The input phone number in various formats.

        Return: str The normalized phone number or an empty string if invalid.
        """
        try:
            phone_number = phone_number.strip().replace(" ","")
            phone_number = phone_number[phone_number.index("0"):]
            found_number = re.fullmatch(r"(\d{3})[\s\t()\n-]*(\d{3})[\s\t()\n-]*(\d{2})[\s\t()\n-]*(\d{2})", phone_number)
            found_number = f"+38{found_number[0]}"
            _ = found_number[12]  # Test if the string is long enough
            return found_number
        except:
            raise ValueError("Invalid phone number format. Expected format: +380-XXX-XXX-XX-XX.")

class Birthday(Field):
    def __init__(self, value):
        super().__init__(Birthday.__validate_birthday(value))
    
    @staticmethod
    def __validate_birthday(birthday_str: str) -> datetime.date:
        """
        Validate and convert birthday string to a date object.
        :param birthday_str: str The input birthday string in DD.MM.YYYY format.

        Return: datetime.date The validated birthday date.
        """
        try:
            day, month, year = map(int, birthday_str.split('.'))
            return datetime.date(year=year, month=month, day=day)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    """
    Class representing a contact record.
    """
    def __init__(self, name):
        self.name = self.add_name(name)
        self.phones = []
        self.birthday = None

    def add_name(self, name):
        try:
            return Name(name)
        except ValueError as e:
            return False

    def add_phone(self, number):
        try:
            phone = Phone(number)
            if phone in self.phones:
                return False, f"Phone number {number} already exists"
            self.phones.append(phone)
            return True, f"Phone number {number} added"
        except ValueError as e:
            return False, str(e)


    def delete_phone(self, number):
        phone = self.find_phone(number)
        if not phone[0]:
            return False, f"Phone number {number} not found"
        self.phones.remove(phone[1])
        return True, f"Phone number {number} deleted"

    def edit_phone(self, old_number, new_number):
        if self.find_phone(old_number)[0]:
            if self.find_phone(old_number)[1] != Phone(new_number):
                self.delete_phone(old_number)
                self.add_phone(new_number)
                return f"Phone number {old_number} updated to {new_number}"
            else:
                return "New phone number already exists"
        else:
            return "Phone number not found"

    def find_phone(self, number):
        try:
            phone = Phone(number)
        except ValueError:
            return False, f"Phone number {number} is invalid"
        if phone in self.phones:
            return True, phone
        return False, f"Phone number {number} not found"

    def add_birthday(self, birthday_str):
        try:
            self.birthday = Birthday(birthday_str)
            return True, f"Birthday for {self.name.value} added"
        except ValueError as e:
            return False, str(e)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime('%d.%m.%Y')
        return "Birthday not set"

    def birthdays(self):
        if self.birthday:
            return "\n".join([self.birthday.value])
        return "No birthday set"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """
    Class representing an address book.
    """
    def add_contact(self, record: Record):
        try:
            self.data[record.name.value] = record
            return True, "Contact added."
        except AttributeError:
            return False, "Error adding contact: Invalid record name."

    def find_contact(self, name):
        return self.data.get(name)

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found")
    
    # Оновити методи для роботи з контактами
    def get_upcoming_birthdays(self) -> list:
        """
        Get a list of upcoming birthdays within the next 7 days. If the day is a weekend, move it to the next Monday.

        Return: List of dictionaries with 'name' and 'congratulation_date' (%Y.%m.%d) keys.
        """
        # Define date boundaries
        now_date = datetime.datetime.now().date()
        treshold_date = now_date + datetime.timedelta(days=7)
        celebrations = []

        # Check all users and prepare their celebration dates
        for user in self.data.values():
            # Skip users without birthday
            if not user.birthday:
                continue
            # Calculate this year's and next year's (if this year has passed) birthday dates
            this_year_birthday = user.birthday.value.replace(year=datetime.datetime.now().year)
            next_year_birthday = this_year_birthday.replace(year=datetime.datetime.now().year + 1)

            # If birthday is during this year within the next 7 days
            if now_date <= this_year_birthday <= treshold_date:
                if this_year_birthday.weekday() in (5, 6):
                    celebration_date = this_year_birthday + datetime.timedelta(days=(7 - this_year_birthday.weekday())) # Move to next Monday
                else:
                    celebration_date = this_year_birthday
                celebrations.append({'name': user.name.value, 'congratulation_date': celebration_date.strftime("%Y.%m.%d")})
            # If birthday has already passed this year, check next year's birthday
            elif now_date > this_year_birthday and next_year_birthday <= treshold_date:
                if next_year_birthday.weekday() in (5, 6):
                    celebration_date = next_year_birthday + datetime.timedelta(days=(7 - next_year_birthday.weekday())) # Move to next Monday
                else:
                    celebration_date = next_year_birthday
                celebrations.append({'name': user.name.value, 'congratulation_date': celebration_date.strftime("%Y.%m.%d")})
            # Continue searching
            else:
                continue
        return celebrations 

def input_error(func):
    """
    Decorator to handle input errors for command functions.
    """
    expected_num_args = {
        'add_contact': 2,
        'change_phone': 3,
        'show_phone': 1,
        'show_all_contacts': 0,
        'add_birthday': 2,
        'show_birthday': 1,
        'birthdays': 0,
    }
    @wraps(func)
    def wrapper(*args, **kwargs):
        command = func.__name__
        if command in expected_num_args:
            num_args = expected_num_args[command]
            if len(args) != num_args:
                return f"Error: {command}() takes {num_args} positional arguments but {len(args)} were given."
        return func(*args, **kwargs)

    return wrapper

def parse_input(user_input: str):
    """
    Parse user input into command and arguments.
    :param user_input: str The raw input string from the user.

    Return: Tuple of command and list of arguments.
    """
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args

@input_error
def add_contact(*args, book: AddressBook):
    """
    Add a new contact to the address book.
    :param args: list The list of arguments containing name and phone number.
    :param book: AddressBook The address book instance.

    Return: str Confirmation message.
    """
    name, phone, *_ = args
    record = book.find_contact(name)
    message = ""
    if record is None:
        record = Record(name)
        message = book.add_contact(record)
        if message[0] and phone:
            message = record.add_phone(phone)[1]
        else:
            message = message[1]
    return message

@input_error
def change_phone(*args, book: AddressBook):
    """
    Change an existing phone number for a contact.
    :param args: list The list of arguments containing name, old phone number, and new phone number.
    :param book: AddressBook The address book instance.

    Return: str Confirmation message.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find_contact(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."

@input_error
def show_phone(*args, book: AddressBook):
    """
    Show phone numbers for a contact.
    :param args: list The list of arguments containing the contact name.
    :param book: AddressBook The address book instance.

    Return: str The phone numbers or an error message.
    """
    name, *_ = args
    record = book.find_contact(name)
    if record is None:
        return "Contact not found."
    phones = ', '.join(phone.value for phone in record.phones)
    return f"Phone numbers for {name}: {phones}"

@input_error
def show_all_contacts(book: AddressBook):
    """
    Show all contacts in the address book.
    :param book: AddressBook The address book instance.

    Return: str The list of all contacts.
    """
    if not book.data:
        return "Address book is empty."
    result = []
    for record in book.data.values():
        phones = ', '.join(phone.value for phone in record.phones)
        result.append(f"{record.name.value}: {phones}")
    return "\n".join(result)

@input_error
def add_birthday(*args, book: AddressBook):
    """
    Add a birthday to a contact.
    :param args: list The list of arguments containing name and birthday.
    :param book: AddressBook The address book instance.

    Return: str Confirmation message.
    """
    name, birthday_str, *_ = args
    record = book.find_contact(name)
    if record is None:
        return "Contact not found."
    return record.add_birthday(birthday_str)[1]

@input_error
def show_birthday(*args, book: AddressBook):
    """
    Show the birthday of a contact.
    :param args: list The list of arguments containing the contact name.
    :param book: AddressBook The address book instance.

    Return: str The birthday or an error message.
    """
    name, *_ = args
    record = book.find_contact(name)
    if record is None:
        return "Contact not found."
    return record.show_birthday()

@input_error
def birthdays(book: AddressBook):
    """
    Show upcoming birthdays within the next 7 days.
    :param book: AddressBook The address book instance.

    Return: str The list of upcoming birthdays.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    result = []
    for entry in upcoming:
        result.append(f"{entry['name']}: {entry['congratulation_date']}")
    return "\n".join(result)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add": # 3 args: command, name, phone
            print(add_contact(*args, book=book))

        elif command in ["change", "update"]: # 4 args: command, name, old_phone, new_phone
            print(change_phone(*args, book=book))

        elif command in ["show", "phone"]: # 2 args: command, name
            print(show_phone(*args, book=book))

        elif command in ["show-all", "all", "contacts"]: # 1 arg: command
            print(show_all_contacts(book=book))

        elif command == "add-birthday": # 3 args: command, name, birthday
            print(add_birthday(*args, book=book))

        elif command in ["birthday", "show-birthday"]: # 2 args: command, name
            print(show_birthday(*args, book=book))

        elif command in ["birthdays", "upcoming-birthdays"]: # 1 arg: command
            print(birthdays(book=book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()