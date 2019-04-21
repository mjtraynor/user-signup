from flask import Flask, request, redirect
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

form = """

<!DOCTYPE html>

<html>
    <head>
        <style>
            .error {{color: red;}}
        </style>
    </head>
    <body>
      <form id="form" action="/register" method="POST">
      <h1>Signup</h1>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" value={0}>
        <span class="error" name="usererror"> {1}</span>
        <p></p>
        <label for="password1">Password</label>
        <input id="password1" name="password1" type="password" {2}>
        <span class="error" name="pass1error"> {3}</span>
        <p></p>
        <label for="password2">Verify Password</label>
        <input id="password2" name="password2" type="password" {4}>
        <span class="error" name="pass2error"> {5}</span>
        <p></p>
        <label for="email">Email (Optional)</label>
        <input id="email" name="email" type="text" value={6}>
        <span class="error" name="emailerror"> {7}</span>
        <p></p>
        <input type="submit" />
      </form>
    </body>
</html>

"""
@app.route("/")
def display_form():
    return form.format("", "", "", "", "", "", "", "")

@app.route("/register", methods=['POST'])
def register():
    user = request.form['username']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    email = request.form['email']

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
        content = form.format(user, userError, pass1, pass1Error,
        pass2, pass2Error, email, emailError)
        return content

    return redirect("/thank_you?user={0}".format(user))

@app.route("/thank_you")
def thank_you():
    user = request.args.get("user")
    return "Thank you for registering, {0}.".format(user)

#@app.route("/", methods=['POST'])
#def register_page():
#    content = form.format("", "", "", "", "", "")

#    return content

app.run()