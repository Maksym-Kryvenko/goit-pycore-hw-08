import pickle
from src.models.address_book import AddressBook
from src.config import DEFAULT_STORAGE_FILENAME


def save_data(book, filename=DEFAULT_STORAGE_FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=DEFAULT_STORAGE_FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
