from getpass import getpass
import mariadb

# Instantiate Connection
try:
  conn = mariadb.connect(
      user=input("Enter your username: "),
      password=getpass("Enter your username: "),
      host="localhost",
      port=3306)
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

# Instantiate Cursor
cur = conn.cursor()
 
#### To be translated in Python #####
CREATE DATABASE happybasil_db;
USE happybasil_db;

CREATE TABLE data (
variable CHAR(20),
value CHAR(20)
);

DESCRIBE data;

INSERT INTO data
(variable, value)
value('light_state', '0');

INSERT INTO data
(variable, value)
value('motor_state', '0');

INSERT INTO data
(variable, value)
value('mode_state', '0');

INSERT INTO data
(variable, value)
value('pi_state', '1');

INSERT INTO data
(variable, value)
value('light', '0');

INSERT INTO data
(variable, value)
value('temp', '0');

INSERT INTO data
(variable, value)
value('humidity', '0');

INSERT INTO data
(variable, value)
value('moisture', '0');

INSERT INTO data
(variable, value)
value('watered', '0');

INSERT INTO data
(variable, value)
value('date', '0');

INSERT INTO data
(variable, value)
value('time', '0');
######################
conn.commit()

# Close Connection
conn.close()
