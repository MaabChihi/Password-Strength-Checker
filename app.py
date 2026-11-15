"""
Website version of the Password Strength Checker.
The checking logic lives in password_checker.py; this file just shows it on a web page.
"""

from flask import Flask, render_template, request

from password_checker import load_common_passwords, check_strength, check_breaches

app = Flask(__name__)
common_passwords = load_common_passwords()


@app.after_request
def no_caching(response):
    """Tell the browser not to save the page, so the result can't be seen in history/cache."""
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    # POST is used so the password never appears in the URL or browser history
    if request.method == "POST":
        password = request.form.get("password", "")

        if password:
            score, rating, tips = check_strength(password, common_passwords)
            try:
                breaches = check_breaches(password)
            except Exception:
                breaches = None  # couldn't reach the API

            # Note: the password itself is never saved or sent back to the page
            result = {"score": score, "rating": rating, "tips": tips, "breaches": breaches}

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(port=5002, debug=False)
