import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Retrieve the stocks owned by the user and the total number of shares owned for each stock
    stocks = db.execute("SELECT symbol, price, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    # Retrieve the cash balance of the user
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate the total value of the portfolio, which is the sum of the cash balance and the value of all the owned stocks
    total = cash

    for stock in stocks:
        total += stock["price"] * stock["shares"]

    # Pass the stocks, cash balance, and total portfolio value to the index.html template to be displayed
    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # If user navigates to the page, display the buy form
    if request.method == "GET":
        return render_template("buy.html")

    # If user submits the form, process the request
    else:
        # Get the symbol and shares from the form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Check if symbol is provided
        if not symbol:
            return apology("Symbol Required!")

        # Lookup the stock information from API
        stock = lookup(symbol.upper())

        # Check if symbol exists
        if stock == None:
            return apology("Symbol Doesn't Exist!")

        # Check if the number of shares is valid
        if shares <= 0:
            return apology("Share Not Allowed!")

        # Calculate the total transaction value
        transaction_value = shares * stock["price"]

        # Get the current user id and cash balance from the database
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        # Check if user has enough balance to complete the transaction
        if user_cash < transaction_value:
            return apology("Insufficient Funds!")

        # Calculate remaining cash after buying the stocks
        remaining_cash = user_cash - transaction_value

        # Update user's cash balance in the database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user_id)

        # Record the transaction in the database
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], date)

        # Flash a success message
        flash("Stocks Bought!")

        # Redirect user to the homepage
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Retrieve the transactions made by the user and order them by date in descending order
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, date FROM transactions WHERE user_id = ? ORDER BY date DESC", user_id)

    # Pass the transactions to the history.html template to be displayed
    return render_template("history.html", transactions=transactions, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if the request method is GET, return the quote.html template
    if request.method == "GET":
        return render_template("quote.html")

    # if the request method is POST
    else:
        # get the symbol from the form submitted
        symbol = request.form.get("symbol")

        # if no symbol is provided, return an apology message
        if not symbol:
            return apology("Symbol Required!")

        # lookup the stock information using the provided symbol
        stock = lookup(symbol.upper())

        # if the stock cannot be found, return an apology message
        if stock == None:
            return apology("Symbol Doesn't Exist!")

        # render the quoted.html template with the stock information
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        # Render the register template if method is GET
        return render_template("register.html")

    else:
        # Get username, password, and confirmation from form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if required fields are not empty
        if not username:
            return apology("Username Required!")
        if not password:
            return apology("Password Required!")
        if not confirmation:
            return apology("Confirm Password!")

        # Check if passwords match
        if password != confirmation:
            return apology("Passwords Don't Match!")

        # Generate hash of the password
        hash = generate_password_hash(password)

        try:
            # Add the new user to the database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            # Return apology if the username already exists
            return apology("Username Already Exists!")

        # Store user ID in session and redirect to index page
        session["user_id"] = new_user
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # Get the user's ID from the session
        user_id = session["user_id"]
        # Get a list of symbols for stocks that the user owns
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id  GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        # Render the sell template and pass in the symbols
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])

    else:
        # Get the symbol and number of shares from the form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure that the symbol and number of shares are valid
        if not symbol:
            return apology("Symbol Required!")
        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Symbol Doesn't Exist!")
        if shares <= 0:
            return apology("Share Not Allowed!")

        # Calculate the total value of the transaction
        transaction_value = shares * stock["price"]

        # Get the user's ID and cash balance from the database
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        # Get the total number of shares the user has for the given stock
        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = :id AND symbol = :symbol AND shares > 0", id=user_id, symbol=symbol)
        user_shares_real = user_shares[0]["total_shares"]

        # Ensure that the user has enough shares to sell
        if shares > user_shares_real:
            return apology("Insufficiant Shares!")

        # Update the user's cash balance in the database
        remaining_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user_id)

        # Add a new transaction to the database to record the sale
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], -shares, stock["price"], date)

        # Show a success message to the user
        flash("Stocks Sold!")

        # Redirect the user to the homepage
        return redirect("/")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add more cash to user account"""

    # If request is GET, render the addCash.html template
    if request.method == "GET":
        return render_template("addCash.html")

    # If request is POST, update the user's cash amount in the database
    else:
        # Get cash amount from form data
        cash_amount = request.form.get("cash_amount")

        # If no cash amount was provided, return an apology
        if cash_amount is None or cash_amount == "":
            return apology("Please Enter Amount")

        # Convert cash amount to an integer
        cash_amount = int(cash_amount)

        # Get user's current cash amount from database
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        # Calculate remaining cash after adding the new amount
        remaining_cash = user_cash + cash_amount

        # Update user's cash amount in the database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user_id)

        # Redirect user to home page
        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow users to change their password"""
    if request.method == "GET":
        return render_template("changePassword.html")
    else:
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Get user info from database
        user_id = session["user_id"]
        user_db = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)

        # Ensure new password and confirmation match
        if new_password != confirm_password:
            return apology("New password and confirmation do not match")

        # Check if old password matches
        if not check_password_hash(user_db[0]["hash"], old_password):
            return apology("Old password is incorrect")

        # Update password hash in database
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=new_hash, id=user_id)

        return redirect("/")

