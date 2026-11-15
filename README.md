# Password Strength Checker & Breach Lookup

A small web app built with **Python (Flask)**, **HTML** and **CSS** that:

1. **Rates a password's strength** (0–5) with a colour bar and tips to improve it
2. **Checks if the password has been leaked** in a real data breach, using the free [Have I Been Pwned](https://haveibeenpwned.com/Passwords) Pwned Passwords service

There's also a command-line version (`password_checker.py`) that uses the same logic.

## How to run it

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5002

**Command-line version** (no install needed):

```bash
python3 password_checker.py
```

**Run the tests:**

```bash
python3 -m unittest -v
```

## How the strength score works

One point each for:
- At least 12 characters
- Lowercase letters
- Uppercase letters
- Numbers
- Symbols

It loses a point for repeating a character 3+ times (e.g. `aaa`), and any password from the common-passwords list scores 0 automatically.

## How the breach check stays private (k-anonymity)

The password is **never sent to the breach service**:

1. The password is hashed with **SHA-1**, e.g. `password` → `5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8`
2. Only the **first 5 characters** (`5BAA6`) are sent to the API
3. The API returns every leaked hash that starts with those 5 characters (hundreds of them)
4. The program checks that list itself to see if the rest of the hash matches

So the service never learns which password was checked.

## Other security choices

| Choice | Why |
|---|---|
| Form uses **POST**, not GET | The password never appears in the URL or browser history |
| `Cache-Control: no-store` header | The browser doesn't save the results page |
| Password is never saved or shown again | Nothing to leak if someone looks at the page or server |
| `type="password"` and `autocomplete="off"` | Password is hidden on screen and not saved by the browser |
| Jinja auto-escaping | Prevents cross-site scripting (XSS) |
| Command line uses `getpass` | Password is hidden as you type |

## Project structure

```
app.py                     Flask website
password_checker.py        Strength + breach checking logic (also runs on its own)
common_passwords.txt       List of very common passwords
templates/index.html       Web page
static/style.css           Styling
test_password_checker.py   Unit tests (unittest)
```

## Possible improvements

- Live strength bar that updates as you type (JavaScript)
- Use a bigger common-passwords list
- Suggest a strong random passphrase
