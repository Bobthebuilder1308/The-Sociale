from flask import Flask, render_template, request, redirect, url_for, flash
import os
import hashlib

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  
USERS_FILE = 'users.txt'
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w'):
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w'):
            pass
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        with open(USERS_FILE, 'a') as f:
            f.write(f'{username},{email},{hashed_password}\n')  
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/plan-hangout', methods=['GET', 'POST'])
def plan_hangout():
    if request.method == 'POST':    
        group_size = request.form['group_size']
        meeting_place = request.form['meeting_place']
        age = request.form['age']
        activity = request.form['activity']
        budget = request.form['budget']
        meeting_range = request.form['meeting_range']
        flash('Hangout planned successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('plan_hangout.html')


def verify_user(username, password):
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user_info = line.strip().split(',')
            if user_info[0] == username:
                hashed_password = user_info[2]
                if hashed_password == hash_password(password):
                    return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
