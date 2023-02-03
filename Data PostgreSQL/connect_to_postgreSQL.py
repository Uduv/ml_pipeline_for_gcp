import psycopg2
import pandas as pd

conn = psycopg2.connect(database="db-Unicauca",
                        host="localhost",
                        user="uduv",
                        password="1234",
                        port="5432")

cursor = conn.cursor()


test = cursor.execute("SELECT * FROM tabletest WHERE id = 1")

cursor.execute(" SELECT * FROM public.tabletest \
ORDER BY id ASC ")


df = pd.DataFrame(cursor.fetchall(), columns=['id', 'date', 'l_ipn','r_asn','f'])

print(df)
