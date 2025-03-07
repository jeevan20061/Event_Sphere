from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # ✅ Import CORS
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

app.secret_key = "your_secret_key"  # Required for flash messages

# ✅ MySQL Database Connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="Jeevan@123",  # Change to your MySQL password
        database="user_database1"
    )
    cursor = db.cursor()
    print("✅ Database connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")

# ✅ Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Route for Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        orgname = request.form['orgname']
        orgtype = request.form['orgtype']
        address = request.form['address']
        contactno = request.form['contactno']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        print(f"Received Data: {orgname}, {orgtype}, {address}, {contactno}, {email}, {username}")

        # ✅ Hash the password before storing
        hashed_password = generate_password_hash(password)

        # ✅ Insert user data into the database
        query = "INSERT INTO users (orgname, orgtype, address, contactno, email, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (orgname, orgtype, address, contactno, email, username, hashed_password)

        try:
            cursor.execute(query, values)
            db.commit()
            print("✅ Data inserted successfully!")
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))  # ✅ Redirect to login page
        except mysql.connector.Error as err:
            print(f"❌ Database Insert Error: {err}")
            flash(f"Error: {err}", "danger")

    return render_template('register.html')

# ✅ Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ✅ Check if username exists in database
        cursor.execute("SELECT orgname, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            orgname, stored_password = user
            if check_password_hash(stored_password, password):
                session['username'] = username
                session['orgname'] = orgname
                flash("Login successful!", "success")
                return redirect(url_for('home'))  # ✅ Redirect to home page
            else:
                flash("Incorrect password!", "danger")
        else:
            flash("Username not found!", "danger")

    return render_template('login.html')

# ✅ Route for Home Page with Event Upload
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        evname = request.form['evname']
        evdate = request.form['evdate']
        evloc = request.form['evloc']
        evwebsite = request.form['evwebsite']
        evimage = request.files['evimage']

        if evimage:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], evimage.filename)
            evimage.save(image_path)  # ✅ Save image file

            # ✅ Insert event data into the database
            query = "INSERT INTO events (evname, evdate, evloc, evwebsite, evimage) VALUES (%s, %s, %s, %s, %s)"
            values = (evname, evdate, evloc, evwebsite, image_path)

            try:
                cursor.execute(query, values)
                db.commit()
                flash("Event uploaded successfully!", "success")
            except mysql.connector.Error as err:
                flash(f"Database Insert Error: {err}", "danger")

    return render_template('home.html', orgname=session['orgname'])

# ✅ Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('orgname', None)
    flash("You have been logged out!", "info")
    return redirect(url_for('index'))

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
