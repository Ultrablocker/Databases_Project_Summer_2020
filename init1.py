#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='project_1',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for customer register
@app.route('/customer_register')
def registerCustomer():
	return render_template('customer_register.html')
#Define route for staff register
@app.route('/staff_register')
def registerStaff():
	return render_template('staff_register.html')
#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register for customer
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
	#grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    phone_no = request.form['phone_no']
    date_of_birth = request.form['date_of_birth']
    passport_no = request.form['passport_no']
    passport_exp = request.form['passport_exp']
    passport_country = request.form['passport_country']
    state = request.form['state']
    city = request.form['city']
    street = request.form['street']
    building_no = request.form['building_no']
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
	    error = "This user already exists"
	    return render_template('register_customer.html', error = error)
    else:
	    ins = 'INSERT INTO customer VALUES(%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	    cursor.execute(ins, (email, password, name, phone_no, date_of_birth, passport_no, passport_exp, passport_country, state, city, street, building_no))
	    conn.commit()
	    cursor.close()
	    return render_template('index.html')
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
# staff register
def registerAuthStaff():
	#grabs information from the forms
    user_name = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline = request.form['airline']
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE user_name = %s'
    cursor.execute(query, (user_name))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('registerStaff.html', error = error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
        cursor.execute(ins, (user_name, password, first_name, last_name, date_of_birth, airline))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/home')
def home():

    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)