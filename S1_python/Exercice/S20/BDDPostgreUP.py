# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:04:28 2020

@author: Sam
"""


SERVERTYPE="POSTGRESQL"
#SERVERTYPE="MYSQL"

if "MYSQL" == SERVERTYPE :
    DBSERVERNAME="fbanguimysql.mysql.database.azure.com"
    ADMINDBSERVER="admindb@fbanguimysql"
    DBNAME = 'mysqldb'
elif "POSTGRESQL" == SERVERTYPE:
    DBSERVERNAME="samlas.postgres.database.azure.com"
    ADMINDBSERVER="admindb@samlas.postgres.database.azure.com"
    DBNAME="postgres"

DBPASSWD="postgresA-"
DBHOST=DBSERVERNAME
SSLMODE='require'

import pandas as pd
import sqlalchemy
import psycopg2
#import mysql.connector
#from mysql.connector import errorcode

# Update connection string information obtained from the portal
# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".\
format(DBHOST, ADMINDBSERVER, DBNAME, DBPASSWD, SSLMODE)
if SERVERTYPE =="POSTGRESQL" :
    if False :
        conn = psycopg2.connect(conn_string) 
    else :
        conn = psycopg2.connect(host=DBHOST, dbname=DBNAME, user=ADMINDBSERVER, password=DBPASSWD)

    connexion_string = "postgresql://{0}:{1}@{2}/{3}".format(ADMINDBSERVER, DBPASSWD, DBHOST, DBNAME)
elif SERVERTYPE =="MYSQL" :
    # Obtain connection string information from the portal
    config = {
      'host':DBHOST,
      'user':ADMINDBSERVER,
      'password':DBPASSWD,
      'database':DBNAME
    }

    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        print("MYSQL connection established")
        connexion_string = "mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(ADMINDBSERVER, DBPASSWD, DBHOST, DBNAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
      cursor = conn.cursor()
else : 
    print("***ERROR : unknown DB TYPE= {1}".format(SERVERTYPE))
display(connexion_string)
engine = sqlalchemy.create_engine(connexion_string)
engine.connect()

#------------------------------------------

data = [
    {"Col1": 1, "Col2": "A"},
    {"Col1": 2, "Col2": "B"},
    {"Col1": 3, "Col2": "C"}
]

df_test = pd.DataFrame(data)
display(df_test)

df_test.to_sql("table_1", engine, index=False, if_exists="replace")

df_test2 = pd.read_sql("SELECT * FROM train_titanic limit 20", engine)
display(df_test2)