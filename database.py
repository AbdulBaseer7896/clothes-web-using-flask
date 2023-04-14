from sqlalchemy import create_engine, text
import os
import mysql.connector

bd = "mysql+pymysql://lkwp097ctrdqyazqlzcq:pscale_pw_LtMfaJT1s4JfNPi5Q9ck6s2VAqYa8cRbNMsyY4C0x13@aws.connect.psdb.cloud/first-data-base?charset=utf8mb4"
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

  
def add_sign_table_to_db(data):
    with engine.connect() as conn:
      query = text("INSERT INTO sign_table (email_add, password_has, address1, address2, city) VALUES (:email_add, :password_has, :address1, :address2, :city)")

    conn.execute(query, {"email_add": data['email'], "password_has": data["password"], "address1": data["address1"], "address2": data["address2"], "city": data["city"]})

print("This working")
