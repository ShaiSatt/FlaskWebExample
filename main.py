from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "megido_secret_key"
# try try
# Predefined list of users. start with empty list
valid_users = []

# Global variable to store the username. start as "Guest"
current_user = 'Guest'

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html', user=current_user)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        user = request.form['username']
        # Check if the user is valid
        if user in valid_users:
            current_user = user
            flash(" !נכנסת בהצלחה", "success")
            return redirect(url_for('home'))
        else:
            flash(f"משתמש לא קיים {user}", "error")
            return render_template('login.html', user=current_user, message='Invalid username, please try again.')
    return render_template('login.html', user=current_user, message='')

# Route for logging out
@app.route('/logout')
def logout():
    global current_user
    flash(f"התנתקת בהצלחה! {current_user}", "success")
    current_user = 'Guest'
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
    if username in valid_users:
        flash(f"משתמש קיים {username}", "error")
        return render_template('signup.html', user=current_user, message='Username already taken, please choose another.')
    valid_users.append(username)
    flash(f"{username} נרשמת בהצלחה", "success")
    return redirect(url_for('login'))
  
  return render_template('signup.html', user=current_user, message='')

@app.route("/users")
def show_users():
    return render_template("users.html", user=current_user,users=valid_users)
  
if __name__ == '__main__':
    app.run(debug=True)
