from sqlalchemy import create_engine, text
import os


bd = "mysql+pymysql://bcqcnf0mqdgxjcuwtbqr:pscale_pw_VLiReyJTnDZgOJCYKVLzheKwf4KYxQdQupkvUk7EzJB@aws.connect.psdb.cloud/first-data-base?charset=utf8mb4"
engine = create_engine(
  bd , connect_args={
    "ssl":{
      "ssl_ca":"/etc/ssl/cert.pem"
    }
})


def log_in_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from man_image"))
    log_in = []
    for row in result.all():
      log_in.append(row)
    return log_in

# a = load_jobs_from_db()
# print(a)
  
  
def add_sign_table_to_db(data):
    with engine.connect() as conn:
      query = text("INSERT INTO sign_table (email_add, password_has, address1, address2, city) VALUES (:email_add, :password_has, :address1, :address2, :city)")

    conn.execute(query, {"email_add": data['email'], "password_has": data["password"], "address1": data["address1"], "address2": data["address2"], "city": data["city"]})

print("This working")



  
# def sign_store_in_db():
#     with engine.connect() as conn:
          
  
# def get_password():
#     with engine.connect() as conn:
#       result = conn.execute(text("select * from loge_in"))
#       log_in = []
#       for row in result.all():
#         log_in.append(row)
#     return log_in
  