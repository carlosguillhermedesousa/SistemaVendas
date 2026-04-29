import re
import bcrypt
import random
from datetime import datetime
from models.db import query_db


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def clean_digits(value: str) -> str:
    return re.sub(r'\D', '', value or '')


def validate_cpf(value: str) -> bool:
    value = clean_digits(value)
    if len(value) != 11 or len(set(value)) == 1:
        return False
    def calculate_digit(digits):
        s = sum(int(d) * w for d, w in zip(digits, range(len(digits)+1, 1, -1)))
        r = 11 - (s % 11)
        return '0' if r >= 10 else str(r)
    first, second = value[:9], value[:10]
    return value[9] == calculate_digit(first) and value[10] == calculate_digit(second)


def validate_cnpj(value: str) -> bool:
    value = clean_digits(value)
    if len(value) != 14 or len(set(value)) == 1:
        return False
    def calculate_digit(digits, factors):
        s = sum(int(d) * f for d, f in zip(digits, factors))
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    first_factors = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_factors = [6] + first_factors
    first = value[:12]
    second = first + calculate_digit(first, first_factors)
    return value[12] == calculate_digit(first, first_factors) and value[13] == calculate_digit(second, second_factors)


def validate_cpf_cnpj(value: str) -> bool:
    digits = clean_digits(value)
    if len(digits) == 11:
        return validate_cpf(digits)
    if len(digits) == 14:
        return validate_cnpj(digits)
    return False


def generate_cpf() -> str:
    def calculate_digit(digits):
        s = sum(int(d) * w for d, w in zip(digits, range(len(digits)+1, 1, -1)))
        r = 11 - (s % 11)
        return '0' if r >= 10 else str(r)
    
    first = [str(random.randint(0, 9)) for _ in range(9)]
    first.append(calculate_digit(first))
    first.append(calculate_digit(first))
    return ''.join(first)


def generate_cnpj() -> str:
    def calculate_digit(digits, factors):
        s = sum(int(d) * f for d, f in zip(digits, factors))
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    
    first_factors = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_factors = [6] + first_factors
    
    digits = [str(random.randint(0, 9)) for _ in range(12)]
    digits.append(calculate_digit(digits, first_factors))
    digits.append(calculate_digit(digits, second_factors))
    return ''.join(digits)


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def calculate_sale_price(cost_price: float, margin: float) -> float:
    return round(cost_price * (1 + margin / 100.0), 2)


def get_manager_by_password(password: str):
    from models.db import query_db
    users = query_db(
        'SELECT * FROM users WHERE role = ?;',
        ('gerente',)
    )
    for user in users:
        if verify_password(password, user['password']):
            return user
    return None


def to_datetime(value):
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    return value
