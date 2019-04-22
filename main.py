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

    if not user:
        userError = "Username is required"
    elif len(user) < 3 or len(user) > 20:
        userError = "Username must be between 3 and 20 characters"
        user = ""
    else:
        isSpace = False
        for char in user:
            if char == " ":
                isSpace = True
        if isSpace == True:
            userError = "Password must not contain a space"
            user = ""

    if not pass1:
        pass1Error = "Password is required"
    elif len(pass1) < 3 or len(pass1) > 20:
        pass1Error = "Password must be between 3 and 20 characters"
    else:
        isSpace = False
        for char in pass1:
            if char == " ":
                isSpace = True
        if isSpace == True:
            pass1Error = "Password must not contain a space"

    if pass1Error == "":
        if pass1 != pass2:
            pass2Error = "Password 2 must match password"

    if email:
        isdot = False
        isat = False
        for char in email:
            if char == ".":
                isdot = True
            elif char == "@":
                isat = True
        if isdot == False or isat == False:        
            emailError = "Email must contain an @ symbol, and only one . symbol"
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