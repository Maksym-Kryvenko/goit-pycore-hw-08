from src.models.address_book import AddressBook
from src.models.record import Record
from src.utils.decorators import input_error


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
    phones = ", ".join(phone.value for phone in record.phones)
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
        phones = ", ".join(phone.value for phone in record.phones)
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
