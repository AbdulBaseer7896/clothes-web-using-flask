from flask import Flask, request, render_template,  flash, redirect
from database import log_in_from_db
from database import add_man_data_from_db  , add_woman_data_from_db , delete_woman_product_form_db_and_file, order_details_from_db ,delete_man_product_form_db_and_file

from database import engine, text
import os
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
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
        data = order_details_from_db()
        for code in log:
            if email == "abdulbasirqazi@gmail.com" and password == 12345:
                return render_template("admin.html" , data = data)

            if email == code[0] and password == code[1]:
                print(code[0], code[1])
                return render_template("index.html")
    return render_template('log_in.html')


@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    return render_template("admin.html")


@app.route("/Add_man", methods=["GET", "POST"])
def man_page():
    data = add_man_data_from_db()
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
    return render_template("add_man.html" , data = data)


@app.route("/Add_woman", methods=["GET", "POST"] )
def woman_page():
    data = add_woman_data_from_db()
    print("This is woman data" )
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
    return render_template("add_woman.html" , data = data)


app.route("/conformed_order")
def conformed_order():
    return render_template('order_conform.html')


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
    price = request.args.get('price')
    item_name = request.args.get('item_name')
    path = request.args.get('path')
    data = [price , item_name , path]
    return render_template('buy.html' , data = data )


@app.route('/order' ,methods=["GET", "POST"]  )
def order():
    print("this is order_page")
    if request.method == "POST":
        with engine.connect() as conn:
            query = text(
                "INSERT INTO orders (name ,email,phone_num,password,address1,address2,city,province,country,image_name , image_price,image_path ) VALUES (:name , :email, :phone_num, :password, :address1, :address2, :city, :province, :country, :image_name , :image_price , :image_path)")
            if(request.form.get('name') == "" or request.form.get("phone") == "" or request.form.get("address1") == "" ):
                return render_template('buy.html')
            else:
                conn.execute(query, {"name": request.form.get('name'), "email": request.form.get("email"), "phone_num": request.form.get("phone"), "password": request.form.get("password"), "address1": request.form.get("address1") , "address2": request.form.get("address2") ,"city": request.form.get("city") , "province": request.form.get("province"), "country": request.form.get("country") ,  "image_name": request.form.get("item_name") ,  "image_price": request.form.get("price") ,  "image_path": request.form.get("item_path")})

            
            print("value is inserted in database")
            return render_template("order_conform.html")
    return render_template("buy.html")



@app.route('/delete_products_from_woman' ,methods=["GET", "POST" , "DELETE"]  )
def delete_product_woman():
    path = request.args.get('path')
    delete_woman_product_form_db_and_file(path)
    datas = add_woman_data_from_db()
    return render_template('add_woman.html' ,data = datas)



@app.route('/delete_products_from_man' ,methods=["GET", "POST" , "DELETE"]  )
def delete_product_man():
    path = request.args.get('path')
    delete_man_product_form_db_and_file(path)
    datas = add_man_data_from_db()
    return render_template('add_man.html' ,data = datas)

@app.route('/child_page' )
def child():
    return render_template('child.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
