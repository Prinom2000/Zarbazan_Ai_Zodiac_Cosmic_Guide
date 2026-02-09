"""
Numerology Utility Functions
"""


def get_number_value(char: str) -> int:
    """Convert letter to numerology number"""
    char = char.upper()
    values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    return values.get(char, 0)


def reduce_to_single(number: int) -> int:
    """Reduce number to single digit (except master numbers 11, 22, 33)"""
    while number > 9 and number not in [11, 22, 33]:
        number = sum(int(d) for d in str(number))
    return number


def calculate_life_path(birth_date: str) -> int:
    """Calculate life path number from birth date"""
    parts = birth_date.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    
    total = sum(int(d) for d in str(year)) + sum(int(d) for d in str(month)) + sum(int(d) for d in str(day))
    return reduce_to_single(total)


def calculate_destiny_number(full_name: str) -> int:
    """Calculate destiny number from full name"""
    total = sum(get_number_value(c) for c in full_name if c.isalpha())
    return reduce_to_single(total)


def calculate_soul_urge(full_name: str) -> int:
    """Calculate soul urge number from vowels in name"""
    vowels = "AEIOU"
    total = sum(get_number_value(c) for c in full_name.upper() if c in vowels)
    return reduce_to_single(total)