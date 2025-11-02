import re
import datetime


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
        clean_name = name.strip().replace("  ", " ")
        if clean_name.isalpha():
            clean_name = re.findall(r"[A-Za-zА-Яа-яЁёЏїІіЄєҐґ\s]+", clean_name)
            if isinstance(clean_name, list) and clean_name:
                clean_name = clean_name[0]
            if clean_name:
                return clean_name
        raise ValueError(
            "Invalid name format. Name should contain only letters and spaces"
        )


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
            phone_number = phone_number.strip().replace(" ", "")
            phone_number = phone_number[phone_number.index("0") :]
            found_number = re.fullmatch(
                r"(\d{3})[\s\t()\n-]*(\d{3})[\s\t()\n-]*(\d{2})[\s\t()\n-]*(\d{2})",
                phone_number,
            )
            found_number = f"+38{found_number[0]}"
            _ = found_number[12]  # Test if the string is long enough
            return found_number
        except:
            raise ValueError(
                "Invalid phone number format. Expected format: +380-XXX-XXX-XX-XX."
            )


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
            day, month, year = map(int, birthday_str.split("."))
            return datetime.date(year=year, month=month, day=day)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
