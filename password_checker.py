"""
Password Strength Checker and Breach Lookup

1. Rates how strong a password is and explains how to improve it.
2. Checks if the password has appeared in a known data breach using the
   free Have I Been Pwned "Pwned Passwords" service.

The full password is NEVER sent over the internet. We hash it with SHA-1
and only send the first 5 characters of the hash (this is called k-anonymity).
"""

import getpass
import hashlib
import os
import string
import urllib.request

API_URL = "https://api.pwnedpasswords.com/range/"
COMMON_PASSWORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common_passwords.txt")


def load_common_passwords():
    """Read the list of common passwords into a set (fast to search)."""
    with open(COMMON_PASSWORDS_FILE) as f:
        return {line.strip().lower() for line in f if line.strip()}


def check_strength(password, common_passwords):
    """
    Give the password a score from 0 to 5 and a list of tips.
    Returns (score, rating, tips).
    """
    score = 0
    tips = []

    # Common passwords are always weak, no matter what
    if password.lower() in common_passwords:
        return 0, "Very weak", ["This is one of the most common passwords. Never use it."]

    if len(password) >= 12:
        score += 1
    else:
        tips.append("Use at least 12 characters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        tips.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        tips.append("Add symbols like ! @ # $ %.")

    # Lose a point for long runs of the same character, e.g. "aaaa"
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            score = max(score - 1, 0)
            tips.append("Avoid repeating the same character 3 or more times.")
            break

    ratings = ["Very weak", "Very weak", "Weak", "Okay", "Strong", "Very strong"]
    return score, ratings[score], tips


def sha1_hash(password):
    """Return the SHA-1 hash of the password in uppercase hex."""
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def count_in_response(hash_suffix, response_text):
    """
    The API returns lines like 'SUFFIX:COUNT'.
    Find our suffix and return how many times it was seen (0 if not found).
    """
    for line in response_text.splitlines():
        suffix, count = line.split(":")
        if suffix == hash_suffix:
            return int(count)
    return 0


def check_breaches(password):
    """Return how many times this password appears in known breaches."""
    full_hash = sha1_hash(password)
    prefix, suffix = full_hash[:5], full_hash[5:]

    request = urllib.request.Request(API_URL + prefix, headers={"User-Agent": "Password-Checker-Student-Project"})
    with urllib.request.urlopen(request, timeout=10) as response:
        text = response.read().decode("utf-8")

    return count_in_response(suffix, text)


def main():
    print("=== Password Strength Checker ===")
    print("Your password is hidden as you type and is never stored or sent in full.\n")

    common_passwords = load_common_passwords()

    while True:
        password = getpass.getpass("Enter a password to check (or press Enter to quit): ")
        if password == "":
            print("Goodbye!")
            break

        score, rating, tips = check_strength(password, common_passwords)
        print(f"\nStrength: {rating} ({score}/5)")
        for tip in tips:
            print(f"  - {tip}")

        try:
            times_found = check_breaches(password)
            if times_found > 0:
                print(f"\nWARNING: This password has appeared in {times_found:,} data breaches. Do not use it!")
            else:
                print("\nGood news: this password was not found in any known breaches.")
        except Exception:
            print("\nCould not reach the breach database. Check your internet connection.")

        print()


if __name__ == "__main__":
    main()
