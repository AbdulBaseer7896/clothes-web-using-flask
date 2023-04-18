from sqlalchemy import create_engine, text
import os
import mysql.connector

nothing = os.environ.get('db_connection')

bd = nothing
engine = create_engine(
  bd , connect_args={
    "ssl":{
      "ssl_ca":"/etc/ssl/cert.pem"
    }
})


def log_in_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from sign_table"))
    log_in = []
    for row in result.all():
      log_in.append(row)
    return log_in


def add_man_data_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from add_man"))
    return result
  

def add_woman_data_from_db():
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from add_woman"))
    return result


def order_details_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from orders"))
    return result  
  
   
  
  
def delete_woman_product_form_db_and_file(path):
    with engine.connect() as conn:
        query = text("DELETE FROM add_woman WHERE pic_name = :path")
        values = {'path': path}
        result = conn.execute(query, values)
    os.remove(f"static/{path}")
    return result
  
  
def delete_man_product_form_db_and_file(path):
    with engine.connect() as conn:
        query = text("DELETE FROM add_man WHERE pic_name = :path")
        values = {'path': path}
        result = conn.execute(query, values)
    os.remove(f"static/{path}")
    return result
  
  
  
def add_sign_table_to_db(data):
    with engine.connect() as conn:
      query = text("INSERT INTO sign_table (email_add, password_has, address1, address2, city) VALUES (:email_add, :password_has, :address1, :address2, :city)")

    conn.execute(query, {"email_add": data['email'], "password_has": data["password"], "address1": data["address1"], "address2": data["address2"], "city": data["city"]})

print("This working")
