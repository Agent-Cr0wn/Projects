from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    