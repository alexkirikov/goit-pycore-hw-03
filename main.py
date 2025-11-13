import datetime
import random
import re


# ======== Завдання 1 ========

def get_days_from_today(date: str) -> int:
    """
    Повертає кількість днів між заданою датою та сьогодні.
    Дата у форматі 'YYYY-MM-DD'.
    """

    try:
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Неправильний формат дати. Використовуйте 'YYYY-MM-DD'.")

    today = datetime.date.today()
    delta = today - target_date
    return delta.days


# ======== Завдання 2 ========

def get_numbers_ticket(min_value: int, max_value: int, quantity: int) -> list:
    """
    Генерує список унікальних випадкових чисел.
    """

    if (
        not isinstance(min_value, int)
        or not isinstance(max_value, int)
        or not isinstance(quantity, int)
        or min_value < 1
        or max_value > 1000
        or min_value > max_value
        or quantity > (max_value - min_value + 1)
        or quantity <= 0
    ):
        return []

    result = sorted(random.sample(range(min_value, max_value + 1), quantity))
    return result


# ======== Завдання 3 ========

def normalize_phone(phone_number: str) -> str:
    """
    Нормалізує номер телефону в стандарт: +380XXXXXXXXX.
    Видаляє всі символи, крім цифр і '+'.
    """
    normalized = ""

    # Прибираємо зайві символи
    clean = re.sub(r"[^\d+]", "", phone_number)

    # Якщо починається з '+380' ок
    if clean.startswith("+380"):
        normalized = clean

    # Якщо починається з '380' додаємо '+'
    elif clean.startswith("380"):
        normalized = "+" + clean

    # Якщо немає коду додаємо '+38'
    # Залишаємо тільки цифри
    else:
        digits = re.sub(r"\D", "", phone_number)
        normalized = "+38" + digits

    # Перевіряємо довжину
    if len(normalized) != 13:
        raise ValueError(f"Невірний номер: {normalized}. Очікувана довжина — 13 символів")

    return normalized

# ======== Завдання 4 ========

def get_upcoming_birthdays(users: list) -> list:
    """
    Повертає список працівників, яких потрібно привітати за 7 днів, включно з сьогодні.
    Якщо день народження припадає на вихідний — привітання переноситься на понеділок.
    """

    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=7)

    upcoming = []

    for user in users:

        try:
            bday = datetime.datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        except ValueError:
            continue  # некоректна дата - пропускаємо

        birthday_this_year = bday.replace(year=today.year)

        # Якщо вже було - беремо наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Перевіряємо чи в межах 7 днів
        if today <= birthday_this_year <= end_date:

            congratulation_date = birthday_this_year

            # Перенос на понеділок, якщо вихідний
            if congratulation_date.weekday() == 5:     # це субота
                congratulation_date += datetime.timedelta(days=2)
            elif congratulation_date.weekday() == 6:   # це неділя
                congratulation_date += datetime.timedelta(days=1)

            upcoming.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming


# ======== Тести ========

if __name__ == "__main__":
    # Завдання 1
    print(get_days_from_today("2020-10-09"))

    # Завдання 2
    print(get_numbers_ticket(1, 49, 6))

    # Завдання 3
    raw_numbers = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
        "12345",                 #  некоректний  короткий
        "+38050123456789"        #  некоректний довгий
    ]

    for num in raw_numbers:
        try:
            cleared = normalize_phone(num)
            print(f"OK: {num!r} --> {cleared}")
        except ValueError as e:
            print(f"ERROR: {num!r} --> {e}")

    # Завдання 4
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"}
    ]
    print(get_upcoming_birthdays(users))

