# Default filename for storing the address book data
DEFAULT_STORAGE_FILENAME = "data/addressbook.pkl"

# Number of days to look ahead for upcoming birthdays
UPCOMING_BIRTHDAYS_DAYS = 7

# Config to check passed arguments
EXPECTED_NUM_ARGS = {
        "add_contact": 2,
        "change_phone": 3,
        "show_phone": 1,
        "show_all_contacts": 0,
        "add_birthday": 2,
        "show_birthday": 1,
        "birthdays": 0,
    }