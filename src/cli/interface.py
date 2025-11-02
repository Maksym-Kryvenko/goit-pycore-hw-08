from src.cli.parser import parse_input
from src.cli.commands import (
    add_contact,
    change_phone,
    show_phone,
    show_all_contacts,
    add_birthday,
    show_birthday,
    birthdays,
)
from src.services.storage import save_data, load_data


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

        elif command == "add":  # 3 args: command, name, phone
            print(add_contact(*args, book=book))

        elif command in [
            "change",
            "update",
        ]:  # 4 args: command, name, old_phone, new_phone
            print(change_phone(*args, book=book))

        elif command in ["show", "phone"]:  # 2 args: command, name
            print(show_phone(*args, book=book))

        elif command in ["show-all", "all", "contacts"]:  # 1 arg: command
            print(show_all_contacts(book=book))

        elif command == "add-birthday":  # 3 args: command, name, birthday
            print(add_birthday(*args, book=book))

        elif command in ["birthday", "show-birthday"]:  # 2 args: command, name
            print(show_birthday(*args, book=book))

        elif command in ["birthdays", "upcoming-birthdays"]:  # 1 arg: command
            print(birthdays(book=book))

        else:
            print("Invalid command.")
