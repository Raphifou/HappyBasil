from getpass import getpass
import mariadb
# Your DB needs to be created before launching this script
# In your SQL envirnement:
#CREATE DATABASE happybasil_db;
#USE happybasil_db;
#CREATE TABLE data (variable CHAR(20),value CHAR(20));
while True:
    value = raw_input("Did you create the HapPyBasil databse ? [Y/n]").lower()
       if value == 'y':
          break
       elif value == 'n':
        print ("Please, go to your SQL consol and create your database")
        break
       else:
        continue
# Instantiate Connection
try:
  conn = mariadb.connect(
      user=input("Enter your username: "),
      password=getpass("Enter your username: "),
      host="localhost",
      port=3306,
  		database=input("Enter your database name: "),
		  autocommit=True)
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

print ("Connected to the happybasil database")
print ("Filling the database...")
# Instantiate Cursor
cur = conn.cursor()

#### To be translated in Python #####
cur.execute(INSERT INTO data (variable, value) value('light_state', '0'))

cur.execute(INSERT INTO data (variable, value) value('motor_state', '0'))

cur.execute(INSERT INTO data (variable, value) value('mode_state', '0'))

cur.execute(INSERT INTO data (variable, value) value('pi_state', '1'))

cur.execute(INSERT INTO data (variable, value) value('light', '0'))

cur.execute(INSERT INTO data (variable, value) value('temp', '0'))

cur.execute(INSERT INTO data (variable, value) value('humidity', '0'))

cur.execute(INSERT INTO data (variable, value) value('moisture', '0'))

cur.execute(INSERT INTO data (variable, value) value('watered', '0'))

cur.execute(INSERT INTO data (variable, value) value('date', '0'))

cur.execute(INSERT INTO data (variable, value) value('time', '0'))

print ("The database has been filled !")

# Close Connection
conn.close()
