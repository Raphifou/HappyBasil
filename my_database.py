import os
import mariadb

#Set up the database
def	clear_db(light, motor, mode, pi):
  try:
    statement = "INSERT INTO variables (light_state, motor_state, mode_state, pi_state) VALUES (light, motor, mode, pi)"
    data = (light, motor, mode, pi)
    cursor.execute(statement, data)
    connection.commit()
    print("Successfully added entry to database")
    except database.Error as e:
      print(f"Error adding entry to database: {e}")

def read_db(light_state, motor_state,mode_state,pi_state):

def update_db(temp, light, humidity, moisture, curr_time, curr_date):
    try:
        statement = "INSERT INTO employees (first_name,last_name) VALUES (%s, %s)"
        data = (first_name, last_name)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")
