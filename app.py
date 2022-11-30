import sqlite3
import random
from flask import Flask, session, render_template, request, g, flash, url_for, redirect

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"
app.config["SESSION_COOKIE_NAME"] = "myCOOKIE_monSTER528"


@app.route("/")
def index():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/orders", methods=["POST", "GET"])
def orders():
    session["all_items"], session["shopping_items"] = get_db()
    return render_template("index.html",all_items=session["all_items"], shopping_items=session["shopping_items"] )

@app.route("/add_items", methods=["POST"])
def add_items():
    session["shopping_items"].append(request.form["select_items"])
    session.modified = True
    return render_template("index.html", all_items=session["all_items"], shopping_items=session["shopping_items"])


@app.route("/remove_items", methods=["POST"])
def remove_items():
    check_boxes = request.form.getlist("check")

    for item in check_boxes:
        if item in session["shopping_items"]:
            idx = session["shopping_items"].index(item)
            session["shopping_items"].pop(idx)
            session.modified = True
    return render_template("index.html", all_items=session["all_items"],
                                         shopping_items=session["shopping_items"])



def register_user_to_db(username, password):
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("insert into users(username, password) values(?,?)", (username, password))
    con.commit()
    con.close()

def check_user(username, password):
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("select username,password from users where username=? and password=?", (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


def get_db():
    db = getattr(g, '_datbase', None)
    if db is None:
        db = g._database = sqlite3.connect("games.db")
        cursor = db.cursor()
        cursor.execute("Select name from games")
        all_data = cursor.fetchall()
        all_data = [str(val[0]) for val in all_data]

        shopping_list = all_data.copy()
        random.shuffle(shopping_list)
        shopping_list = shopping_list[:5]
    return all_data, shopping_list

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == ('__main__'):
    app.run(debug=True)
