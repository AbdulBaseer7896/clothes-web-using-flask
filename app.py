from flask import Flask, request, render_template,  flash, redirect
from database import log_in_from_db
from database import add_man_data_from_db  , add_woman_data_from_db
from database import engine, text
import os
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route("/sign_in")
def sign_page():
    return render_template("sign_page.html")


@app.route("/sign", methods=["GET", "POST"])
def sign_page_for():
    print("this is sign_page")
    if request.method == "POST":
        with engine.connect() as conn:
            query = text(
                "INSERT INTO sign_table (email__add, password_has, address1, address2, city) VALUES (:email__add, :password_has, :address1, :address2, :city)")

            conn.execute(query, {"email__add": request.form.get('email'), "password_has": request.form.get(
                "password"), "address1": request.form.get("address1"), "address2": request.form.get("address2"), "city": request.form.get("city")})
            print("value is inserted in database")
            return render_template("log_in.html")
    return render_template("sign_page.html")


@app.route("/log_in", methods=["GET", "POST"])
def log_page():
    print("thisis log_page now")
    if request.method == "POST":
        email = request.form.get("email")
        password = int(request.form.get("password"))
        log = log_in_from_db()
        print("THis is code ")
        print(log)
        for code in log:
            if email == "abdulbasirqazi@gmail.com" and password == 12345:
                return render_template("admin.html")

            if email == code[0] and password == code[1]:
                print(code[0], code[1])
                return render_template("index.html")
    return render_template('log_in.html')


@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    return render_template("admin.html")


@app.route("/Add_man", methods=["GET", "POST"])
def man_page():
    file = request.files.get('avatar')
    if file is not None:
        new_filename = str(datetime.now().timestamp()).replace(
            ".", "")  # Generating unique name for the file
        # Spliting ORIGINAL filename to seperate extenstion
        split_filename = file.filename.split(".")
        # Canlculating last index of the list got by splitting the filname
        ext_pos = len(split_filename)-1
        # Using last index to get the file extension
        ext = split_filename[ext_pos]
        db_path = str(f"uploads/add_man/{new_filename}.{ext}")
        print("The type of path  = ", type(db_path))
        file.save(f"static/uploads/add_man/{new_filename}.{ext}")

        print("File uploaded successfully")
        print(request.form.get('name'), request.form.get("price"))
        if request.method == 'POST':
            print("post work")
            with engine.connect() as conn:
                query = text(
                    "INSERT INTO add_man (item_name, price, descp , pic_name) VALUES (:item_name, :price, :descp, :pic_name)")
                print("its between")
                conn.execute(query, {"item_name": request.form.get('name'), "price": int(request.form.get(
                    "price")), "descp": request.form.get("description"), "pic_name": db_path})
                print("Data inserted successfully")
    else:
        print("Error: No file uploaded")
    return render_template("add_man.html")


@app.route("/Add_woman", methods=["GET", "POST"] )
def woman_page():
    file = request.files.get('avatar')
    if file is not None:
        new_filename = str(datetime.now().timestamp()).replace(
            ".", "")  # Generating unique name for the file
        # Spliting ORIGINAL filename to seperate extenstion
        split_filename = file.filename.split(".")
        # Canlculating last index of the list got by splitting the filname
        ext_pos = len(split_filename)-1
        # Using last index to get the file extension
        ext = split_filename[ext_pos]
        db_path = str(f"uploads/add_woman/{new_filename}.{ext}")
        print("The type of path  = ", type(db_path))
        file.save(f"static/uploads/add_woman/{new_filename}.{ext}")

        print("File uploaded successfully")
        print(request.form.get('name'), request.form.get("price"))
        if request.method == 'POST':
            print("post work")
            with engine.connect() as conn:
                query = text(
                    "INSERT INTO add_woman (item_name, price, descp , pic_name) VALUES (:item_name, :price, :descp, :pic_name)")
                print("its between")
                conn.execute(query, {"item_name": request.form.get('name'), "price": int(request.form.get(
                    "price")), "descp": request.form.get("description"), "pic_name": db_path})
                print("Data inserted successfully")
    else:
        print("Error: No file uploaded")
    return render_template("add_woman.html")


# def add_man_data_from_db():
#   with engine.connect() as conn:
#     result = conn.execute(text("select * from add_man"))
#     log_in = []
#     for row in result.all():
#       log_in.append(row)
#     return log_in


@app.route("/man-page" , methods=["GET", "POST"])
def man():
    print("its work")
    data = add_man_data_from_db()
    print("This is data")
    print(data)
    return render_template("man.html" , images = data)


@app.route("/woman-page" , methods=["GET", "POST"])
def woman():
    print("its work")
    data = add_woman_data_from_db()
    print("This is data")
    print(data)
    return render_template("woman.html" , images = data)


@app.route("/buy" , methods=["GET", "POST"] )
def buy():
    number = str(request.args.get('number'))
    print(number)
    return render_template('buy.html' , number = number)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
