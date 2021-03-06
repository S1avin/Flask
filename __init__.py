from flask import Flask, render_template, request, url_for, redirect, session
from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
 
app = Flask(__name__)

@app.route('/')
def homepage():

    title = "Empty page"
    paragraph = ["Nothing here right now"]

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception as e:
        return str(e)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route('/new')
def nawpage():

    title = "Add new Item"
    paragraph = ["Here will be some input boxes."]

    return render_template("index.html", title=title, paragraph=paragraph)


@app.route('/update')
def updatePage():

    title = "update"
    paragraph = ["update"]

    return render_template("index.html", title=title, paragraph=paragraph)


@app.route('/update/title')
def updatetitlePage():

    title = "update title"
    paragraph = ["You can update any title here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/price')
def updatepricePage():

    title = "update price"
    paragraph = ["You can update any price here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/description')
def updatedescriptionPage():

    title = "update description"
    paragraph = ["You can update any description here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/update/location')
def updatelocationPage():

    title = "update location"
    paragraph = ["You can update any location here"]

    return render_template("index.html", title=title, paragraph=paragraph)

@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
	
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)  

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    

@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('new'))

        return render_template("register.html", form=form)

    except Exception as e:
        return("Error: " + str(e))
 
if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
