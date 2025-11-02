from collections import UserDict
import datetime
from src.config import UPCOMING_BIRTHDAYS_DAYS


class AddressBook(UserDict):
    """
    Class representing an address book.
    """

    def add_contact(self, record):
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
        treshold_date = now_date + datetime.timedelta(days=UPCOMING_BIRTHDAYS_DAYS)
        celebrations = []

        # Check all users and prepare their celebration dates
        for user in self.data.values():
            # Skip users without birthday
            if not user.birthday:
                continue
            # Calculate this year's and next year's (if this year has passed) birthday dates
            this_year_birthday = user.birthday.value.replace(
                year=datetime.datetime.now().year
            )
            next_year_birthday = this_year_birthday.replace(
                year=datetime.datetime.now().year + 1
            )

            # If birthday is during this year within the next 7 days
            if now_date <= this_year_birthday <= treshold_date:
                if this_year_birthday.weekday() in (5, 6):
                    celebration_date = this_year_birthday + datetime.timedelta(
                        days=(7 - this_year_birthday.weekday())
                    )  # Move to next Monday
                else:
                    celebration_date = this_year_birthday
                celebrations.append(
                    {
                        "name": user.name.value,
                        "congratulation_date": celebration_date.strftime("%Y.%m.%d"),
                    }
                )
            # If birthday has already passed this year, check next year's birthday
            elif now_date > this_year_birthday and next_year_birthday <= treshold_date:
                if next_year_birthday.weekday() in (5, 6):
                    celebration_date = next_year_birthday + datetime.timedelta(
                        days=(7 - next_year_birthday.weekday())
                    )  # Move to next Monday
                else:
                    celebration_date = next_year_birthday
                celebrations.append(
                    {
                        "name": user.name.value,
                        "congratulation_date": celebration_date.strftime("%Y.%m.%d"),
                    }
                )
            # Continue searching
            else:
                continue
        return celebrations
