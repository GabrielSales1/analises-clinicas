from flask import Flask, render_template,url_for,redirect

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


