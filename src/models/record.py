from .fields import Name, Phone, Birthday


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
            return self.birthday.value.strftime("%d.%m.%Y")
        return "Birthday not set"

    def birthdays(self):
        if self.birthday:
            return "\n".join([self.birthday.value])
        return "No birthday set"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
