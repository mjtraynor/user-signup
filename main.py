from flask import Flask, request

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
      <form action="/register" id="form" form method="POST">
      <h1>Signup</h1>
        <label for="username">Username</label>
        <input name="username" type="text" value={usererror}> 
        <p></p>
        <label for="password1">Password</label>
        <input name="password1" type="text" value={pass1error}>
        <p></p>
        <label for="password2">Verify Password</label>
        <input name="password2" type="text" value={pass2error}>
        <p></p>
        <label for="email">Email (Optional)</label>
        <input name="email" type="text" value={pass3error}>
        <p></p>
        <input type="submit">
      </form>
    </body>
</html>

"""

@app.route("/")
def index():
    return form.format("")

@app.route("/", methods=['POST'])
def validate():

    text = request.form['text']
    rot = int(request.form['rot'])

    encrypt_string = rotate_string(text, rot)

    return form.format(encrypt_string)

app.run()