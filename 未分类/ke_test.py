# -*- coding: utf-8 -*-
import pymysql

connection = pymysql.connect(
    host="10.53.1.177",
    user="root",
    password="yP5pH4pA",
    database="mysql",
    port=3306
)

cursor = connection.cursor()
cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
connection.close()
