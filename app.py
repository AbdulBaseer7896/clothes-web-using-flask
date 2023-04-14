from flask import Flask ,request, render_template ,  flash , redirect
from database import log_in_from_db , add_sign_table_to_db
from database import engine , text 
import os

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route("/sign_in")
def sign_page():
    return render_template("sign_page.html")



@app.route("/sign"  , methods =["GET" ,"POST"])
def sign_page_for():
    print("this is sign_page")
    if request.method == "POST":
        with engine.connect() as conn:
            query = text("INSERT INTO sign_table (email__add, password_has, address1, address2, city) VALUES (:email__add, :password_has, :address1, :address2, :city)")

            conn.execute(query, {"email__add": request.form.get('email'), "password_has": request.form.get("password"), "address1": request.form.get("address1"), "address2": request.form.get("address2"), "city": request.form.get("city")})
            return render_template("log_in.html")
    return render_template("sign_page.html")
        


@app.route("/log_in" , methods =["GET", "POST"])
def log_page():
    print("thisis log_page now")    
    if request.method == "POST":
        email = request.form.get("email")
        password = int(request.form.get("password"))
        log = log_in_from_db()
        for code in log:
            if email == "abdulbasirqazi@gmail.com" and password == 12345:
                return render_template("admin.html")
            if email == code[0] and password == code[1]:
                return render_template("index.html")
    return render_template('log_in.html')


@app.route("/admin"  , methods =["GET", "POST"])
def admin_page():
    return render_template("admin.html")


@app.route("/Add_man")
def man_page():
    return render_template("add_man.html")

@app.route("/Add_woman")
def woman_page():
    return render_template("add_woman.html")



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)












