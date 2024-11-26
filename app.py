from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
# Getting the database for the learners, tutors and session bookings for the website
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/313397/OneDrive - Milton Keynes College O365/Task 2 (Summer 22)/GibJohn_Tutoring_DB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Used for managing Flask-Login for logging a user in and out
login_manager = LoginManager()
login_manager.init_app(app)
# Used to get the ID for the user
login_manager.id_attribute = "get_id"

class Base(DeclarativeBase):
    pass
# Used to create a class for the session bookings table in the database for the booking ID, subject, time, date, learner ID and tutor ID
# Specifies the data type for each of the fields and primary key, foreign key, autoincrement or null
class Session_Bookings(db.Model):
    __tablename__ = 'Session_Bookings'
    booking_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(100))
    time: Mapped[str] = mapped_column(String(100))
    date: Mapped[str] = mapped_column(String(100))
    learner_id: Mapped[int] = mapped_column(Integer, ForeignKey('Learners.learner_id'), nullable=False)
    tutor_id: Mapped[int] = mapped_column(Integer, ForeignKey('Tutors.tutor_id'), nullable=False)
# Used to create a class for the learners table in the database for the learner ID, name, email and password
# Specifies the data type for each of the fields and primary key, foreign key, autoincrement or null
class Learners(UserMixin, db.Model):
    __tablename__ = 'Learners'
    learner_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(1000))


# Used to create a class for the tutors table in the database for the tutor ID, name, email and password
# Specifies the data type for each of the fields and primary key, foreign key, autoincrement or null
# class Tutors():
    # __tablename__ = 'Tutors'
    # tutor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # name: Mapped[str] = mapped_column(String(100), unique=True)
    # email: Mapped[str] = mapped_column(String(100))
    # password: Mapped[str] = mapped_column(String(1000))

# Return the booking ID of a session
    def __repr__(self):
        return f'<Session {self.booking_id}>'
# Return the learner ID of a learner
    def get_id(self):
        return str(self.learner_id)

# Loads a user and gets the user from the database
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Learners, int(user_id))


with app.app_context():
    db.create_all()
# Routes to the home page if the website is opened
@app.route("/")
def index():
    return render_template("index.html", logged_in=current_user.is_authenticated)
# Routes to the about us page if a user clicks on about us
@app.route("/about_us")
def about_us():
    return render_template("about_us.html", logged_in=current_user.is_authenticated)
# Routes to the index page if a user clicks on home when on another page
@app.route("/index")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)
# Routes to the contact us page if a user clicks on contact us
@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html", logged_in=current_user.is_authenticated)
# Routes to the learning resources tools page if a user clicks on learning resources/tools
@app.route("/learning_resources_tools")
def learning_resources_tools():
    if not current_user.is_authenticated: # Checks if a user isn't logged in when accessing the page
        flash("You must be logged in to access this page")
        return redirect(url_for('login')) # Redirects to the login page if a user isn't logged in
    return render_template("learning_resources_tools.html", logged_in=current_user.is_authenticated)
# Routes to the learner progress page if a user clicks on learner progress
@app.route("/learner_progress")
def learner_progress():
    if not current_user.is_authenticated: # Checks if a user isn't logged in when accessing the page
        flash("You must be logged in to access this page")
        return redirect(url_for('login')) # Redirects to the login page if a user isn't logged in
    return render_template("learner_progress.html", logged_in=current_user.is_authenticated)
# Routes to the gamified learning page if a user clicks on gamified learning
@app.route("/gamified_learning")
def gamified_learning():
    if not current_user.is_authenticated: # Checks if a user isn't logged in when accessing the page
        flash("You must be logged in to access this page")
        return redirect(url_for('login')) # Redirects to the login page if a user isn't logged in
    return render_template("gamified_learning.html", logged_in=current_user.is_authenticated)
# Routes to the sessions booking page if a user clicks on book a face-to-face session
@app.route("/sessions_booking", methods=['GET', 'POST'])
def sessions_booking():
        if not current_user.is_authenticated: # Checks if a user isn't logged in when accessing the page
            flash("You must be logged in to access this page")
            return redirect(url_for('login')) # Redirects to the login page if a user isn't logged in
        
        if request.method == 'POST':
            session_time = request.form.get('session_time') # Gets the session time chosen from the session time dropdown
            subject = request.form.get('subject') # Gets the subject chosen from the subject dropdown
            day = request.form.get('DD') # Gets the day in DD format from the DD field
            month = request.form.get('MM') # Gets the month in MM format from the MM field
            year = request.form.get('YYYY') # Gets the year in YYYY format from the YYYY field
            date = f"{day}/{month}/{year}" # Converts the date entered by the user into DD/MM/YYYY format
            if day < "01" or day > "31":
                flash("Please enter a day between 01 and 31")
            elif month < "01" or day > "12":
                flash("Please enter a month between 01 and 12")
            elif year < "2024" or year > "2025":
                flash("Please enter a year between 2024 and 2025")
            elif day and month and year != int:
                flash("Please enter the date as DD/MM/YYYY format")
            new_booking = Session_Bookings(
            subject=subject, # gets the subject for the subject field in the database
            time=session_time, # gets the time for the time field in the database
            date=date, # gets the date for the date field in the database
            learner_id=current_user.get_id() # gets the learner ID from the current user
            )
            db.session.add(new_booking) # Adds a new booking to the database
            db.session.commit() # Commits the booking to the database
            return redirect(url_for('success')) # Redirects to the success page after the booking is made
        return render_template("sessions_booking.html", logged_in=current_user.is_authenticated)
# Routes to the quizzes page if a user clicks on quizzes
@app.route("/quizzes")
def quizzes():
    if not current_user.is_authenticated: # Checks if a user isn't logged in when accessing the page
        flash("You must be logged in to access this page")
        return redirect(url_for('login')) # Redirects to the login page if a user isn't logged in
    return render_template("quizzes.html", logged_in=current_user.is_authenticated)
# Routes to the settings page if a user clicks on settings
@app.route("/settings")
def settings():
    return render_template("settings.html", logged_in=current_user.is_authenticated)
# Routes to the login page if a user clicks on log in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email') # Gets the email entered by the user from the email field
        password = request.form.get('password') # Gets the password entered by the user from the password field
        result = db.session.execute(db.select(Learners).where(Learners.email == email)) # Finds the matching user by their email
        user = result.scalar() # Fetches the user
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login')) # Stays on the login page if the email doesn't exist
        elif not check_password_hash(user.password, password):
            flash("Incorrect password, please try again.") # Stays on the login page if the password is incorrect
            return redirect(url_for('login'))
        else:
            login_user(user) # Logs the user in if their email and password are correct
            return redirect(url_for('index')) # Redirects to the home page after the user is logged in
    return render_template("login.html", logged_in=current_user.is_authenticated)
# Routes to the register page if a user clicks on register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email') # Gets the email entered by the user from the email field
        result = db.session.execute(db.select(Learners).where(Learners.email == email)) # Finds the matching user by their email
        user = result.scalar() # Fetches the user
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login')) # Stays on the login page if the user uses an existing email
        hash_and_salted_password = generate_password_hash( # Generates a password hash
            request.form.get('password'), # Gets the password entered by the user from the password field
            method='pbkdf2:sha256', # Method for hashing the password
            salt_length=8 # Number of characters generated for the salt
        )
        new_user = Learners( # new user is equal to learner in learners class
            email=request.form.get('email'), # email in learners database retrieved from email field
            password=hash_and_salted_password, # hashes the password
            name=request.form.get('name'), # Gets the name entered by the user from the name field
        )
        db.session.add(new_user) # Adds a new user to the database
        db.session.commit() # Commits the user to the database
        login_user(new_user) # Logs the user in
        return redirect(url_for("index")) # Redirects to the home page after the user is logged in
    
    return render_template("register.html", logged_in=current_user.is_authenticated)
# Routes to logging out a user
@app.route('/logout')
def logout():
    logout_user() # Logs a user out
    return redirect(url_for('index')) # Redirects to the home page after a user is logged out

if __name__ == "__main__":
    app.run(debug=True)
