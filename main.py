from flask import Flask, request, redirect
import cgi
import os
import jinja2

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def display_form():
    template = jinja_env.get_template("form.html")
    return template.render()

def no_entry(text):
    if not text:
        return " is required."

def length_check(text):
    if len(text) < 3 or len(text) > 20:
        return " must be between 3 and 20 characters."

def no_space(text):
    for char in text:
        if char == " ":
            return " must not contain a space."

def pass2_check(pass1, pass2):
    if pass1 != pass2:
        return "Password 2 must match password."

def email_check(text):
    dotCount = 0
    atCount = 0
    for char in text:
        if char == ".":
            dotCount += 1
        elif char == "@":
            atCount += 1
    if dotCount == 0 or dotCount > 1 or atCount ==  0 or atCount > 1:        
        return "Email must contain one '@' symbol, and one '.' symbol."

@app.route("/register", methods=['POST'])
def register():
    user = cgi.escape(request.form['username'])
    pass1 = cgi.escape(request.form['password1'])
    pass2 = cgi.escape(request.form['password2'])
    email = cgi.escape(request.form['email'])

    userError = ""
    pass1Error = ""
    pass2Error = ""
    emailError = ""

    if no_entry(user):
        userError = "Username" + no_entry(user)
    elif length_check(user):
        userError = "Username" + length_check(user)
        user = ""
    elif no_space(user):
        userError = "Username" + no_space(user)
        user = ""

    if no_entry(pass1):
        pass1Error = "Password" + no_entry(pass1)
    elif length_check(pass1):
        pass1Error = "Password" + length_check(pass1)
    elif no_space(pass1):
        pass1Error = "Password" + no_space(pass1)

    if pass2_check(pass1, pass2):
        pass2Error = pass2_check(pass1, pass2)
    
    if len(email) > 0:
        if length_check(email):
            emailError = "Email" + length_check(email)
            email = ""
        elif no_space(email):
            emailError = "email" + no_space(pass1)
            email = ""
        elif email_check(email):
            emailError = email_check(email)
            email = ""

    if userError or pass1Error or pass2Error or emailError:
        content = jinja_env.get_template("form.html")

        return content.render(username=user, usererror=userError, assword1=pass1, 
        pass1error=pass1Error, password2=pass2, pass2error=pass2Error, email=email, emailerror=emailError)

    return redirect("/thank_you?user={0}".format(user))

@app.route("/thank_you")
def thank_you():
    user = request.args.get("user")
    template = jinja_env.get_template("thanks.html")

    return template.render(user=user)

#@app.route("/", methods=['POST'])
#def register_page():
#    content = form.format("", "", "", "", "", "")

#    return content

app.run()