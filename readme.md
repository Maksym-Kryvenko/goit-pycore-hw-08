# Технiчний опис завдання

☝ В цьому домашньому завданні ви повинні додати функціонал збереження адресної книги на диск та відновлення з диска.

Для цього — ви маєте вибрати pickle протокол серіалізації/десеріалізації даних та реалізувати методи, які дозволять зберегти всі дані у файл і завантажити їх із файлу.

Головна мета, щоб застосунок не втрачав дані після виходу із застосунку та при запуску відновлював їх з файлу. Повинна зберігатися адресна книга з якою ми працювали на попередньому сеансі.

## Завдання:
Реалізуйте функціонал для збереження стану AddressBook у файл при закритті програми і відновлення стану при її запуску.

## Приклади коду, які стануть в нагоді:

Серіалізація з pickle
```python
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
```

Інтеграція збереження та завантаження в основний цикл
```python
def main():
    book = load_data()

    # Основний цикл програми

    save_data(book)  # Викликати перед виходом з програми
```
Ці приклади допоможуть вам у реалізації домашнього завдання.

## Критерії оцінювання:
* Реалізовано протокол серіалізації/десеріалізації даних за допомогою pickle
* Всі дані повинні зберігатися при виході з програми
* При новому сеансі Адресна книга повинна бути у застосунку, яка була при попередньому запуску.


# Структура проекту:
В межах цього домашнього завдання впроваджена наступна структура проекту:
```
goit-pycore-hw-08/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fields.py          # Field, Name, Phone, Birthday
│   │   ├── record.py          # Record class
│   │   └── address_book.py    # AddressBook class
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage.py         # save_data, load_data
│   │   └── contact_service.py # Business logic for contacts
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py        # Command functions (add_contact, change_phone, etc.)
│   │   ├── parser.py          # parse_input function
│   │   └── interface.py       # main() function and user interaction
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py      # input_error decorator
│       └── validators.py      # Validation utilities
├── data/                      # For storing .pkl files
│   └── .gitkeep
├── main.py                    # Entry point (minimal)
├── requirements.txt
├── .gitignore
├── README.md
└── config.py                  # Configuration constants
```