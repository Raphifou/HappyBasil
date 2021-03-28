import sys
import mariadb

############################
#In your terminal:         #
#export username="username"#
#export password="password"#
############################

username = os.environ.get("username")
password = os.environ.get("password")

# Instantiate Connection
try:
  conn = mariadb.connect(
      user="username",
      password="password",
      host="localhost",
      port=3306)
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

# Instantiate Cursor
cur = conn.cursor()
  
CREATE DATABASE happybasil_db;
USE happybasil_db;

CREATE TABLE data (
variables CHAR(20),
value CHAR(20)
);

DESCRIBE data;

INSERT INTO data
(variables, value)
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

conn.commit()

# Close Connection
conn.close()
