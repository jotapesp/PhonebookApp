def null_or_blank(text):
    return text is None or not text.strip()

def validate_integer_range(question, start, end, default=None):
    while True:
        try:
            entry = input(question)
            if null_or_blank(entry) and default is not None:
                entry = default
            value = int(entry)
            if start <= value <= end:
                return value
        except ValueError:
            print(f"Invalid value. Please enter a valid integer value between {start} and {end}.")

def validate_integer_range_or_blank(question, start, end):
    while True:
        try:
            entry = input(question)
            if null_or_blank(entry):
                return None
            value = int(entry)
            if start <= value <= end:
                return value
        except ValueError:
            print(f"Invalid value. Please enter a valid integer value between {start} and {end}.")
