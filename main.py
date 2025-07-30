import re

def check_strength(password):
    length = len(password) >= 8
    upper = bool(re.search(r"[A-Z]", password))
    lower = bool(re.search(r"[a-z]", password))
    digit = bool(re.search(r"\d", password))
    special = bool(re.search(r"[\W_]", password))

    score = sum([length, upper, lower, digit, special])
    
    if score == 5:
        return "Very Strong 💪"
    elif score >= 3:
        return "Moderate 🔐"
    else:
        return "Weak ❌"

if __name__ == "__main__":
    pwd = input("Enter a password to check: ")
    print("Password Strength:", check_strength(pwd))
