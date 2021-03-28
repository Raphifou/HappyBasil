import sys
import mariadb

# Instantiate Connection
try:
  conn = mariadb.connect(
      user="connpy_test",
      password="passwd",
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
variables CHAR(10),
values CHAR(10)
);

DESCRIBE data;

INSERT INTO data
(variables, values)
VALUES('light_state', 0);

INSERT INTO data
(variables, values)
VALUES('motor_state', 0);

INSERT INTO data
(variables, values)
VALUES('mode_state', 0);

INSERT INTO data
(variables, values)
VALUES('pi_state', 0);

INSERT INTO data
(variables, values)
VALUES('light', 0);

INSERT INTO data
(variables, values)
VALUES('temp', 0);

INSERT INTO data
(variables, values)
VALUES('humidity', 0);

INSERT INTO data
(variables, values)
VALUES('moisture', 0);

INSERT INTO data
(variables, values)
VALUES('watered', 0);

INSERT INTO data
(variables, values)
VALUES('date', 0);

INSERT INTO data
(variables, values)
VALUES('time', 0);

# Close Connection
conn.close()
