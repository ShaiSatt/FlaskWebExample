from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "megido_secret_key"

# Global variable to store the username. start as "Guest"
current_user = 'Guest'

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY NOT NULL, 
                 password TEXT NOT NULL, 
                 email TEXT NOT NULL,
                 phone TEXT )''')
    conn.commit()
    conn.close()
  
create_table()

# Function to insert a new user into the database
def insert_user(username, password, email, phone):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()  # Fetch the first row
    if user:
        conn.close()
        return False  # User already exists
    c.execute("INSERT INTO users VALUES (?, ?, ?,?)", (username, password, email, phone))
    conn.commit()
    conn.close()
    return True

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html', user=current_user)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user # currect user is global variable
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()  # Fetch the first row
        if user:
          if user[1] == password:
            current_user = user[0] # user[0] is username
            flash('התחברת בהצלחה!','success')
            return redirect(url_for('home'))
          else: # password is not correct
            flash('password is not correct, please try again.','error')
            return render_template('login.html', user=current_user, message='password is not correct, please try again.')
        else:
          return render_template('login.html', user=current_user, message='Invalid username, please try again.')
        
    # request method is not post
    return render_template('login.html', user=current_user, message='')

# Route for logging out
@app.route('/logout')
def logout():
    global current_user
    current_user = 'Guest'
    flash('התנתקת בהצלחה!','success')
    return redirect(url_for('home'))

# Route for the restricted page
@app.route('/restricted')
def restricted():
  if current_user != 'Guest' :
    return render_template('restricted.html', user=current_user)
  else:
    return '<h1> access denied </h1> '

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    # Check if the username is already taken
    
    if insert_user(username, password, email,phone) != True:    
      return render_template('signup.html', user=current_user, message='Username already taken, please choose another.')
    return redirect(url_for('login'))
  
  # request method is not POST
  return render_template('signup.html', user=current_user, message='')

@app.route("/users")
def show_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("users.html", user=current_user,users=users)

@app.route('/update', methods=['GET', 'POST'])
def update():
  if current_user == 'Guest':
    return '<h1> access denied </h1> '
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE username = ?", (current_user,))
  user = c.fetchone()  # Fetch the first row
  if request.method == 'POST':
    # Update user details in the database
    password = request.form['new_password']
    email = request.form['new_email']
    phone = request.form['new_phone']
    c.execute("UPDATE users SET password=?, email=?, phone=? WHERE username=?", (password, email, phone, user[0]))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))
  
  return render_template('update.html',user=current_user,user_details=user)
@app.route('/delete', methods=['POST'])
def delete():
  global current_user
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute("DELETE FROM users WHERE username=?", (current_user,))
  current_user = 'Guest'
  conn.commit()
  conn.close()
  return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)