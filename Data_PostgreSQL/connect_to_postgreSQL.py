import psycopg2
import pandas as pd

class postgreSQL : 
    def __init__(self) :
        self.connect = self.conn()
        self.cursor = self.connect.cursor()
        self.exec()
        self.export_pasquet()
        
    def conn(self, database="db-Unicauca", host="localhost", user="uduv", password="1234", port="5432") :
        self.connect = psycopg2.connect(
            database=database, 
            host=host, 
            user=user, 
            password=password,
            port=port)
        print(self.connect)
        return self.connect

    def exec(self,query="SELECT * FROM public.bigtable"):
        self.cursor.execute(query)
        self.df = pd.DataFrame(self.cursor.fetchall(), columns=["id","Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount","Class"])
        print(self.df)
        return self.df

    def export_pasquet(self,path="Data_PostgreSQL/Dataset/db_Unicauca_bigtable.parquet") : 
        self.df.to_parquet(path)

    def generate_postgreSQL_parquet() : 
        """Connect to PostgreSQL database and generate a parquet file for the given dataset

        Returns:
            string file_name : file name
            string path_sql_parquet : path to parquet file
        """
        file_name = "db_Unicauca_bigtable.parquet"
        path_sql_parquet = "Data_PostgreSQL/Dataset/db_Unicauca_bigtable.parquet"
        postgreSQL()
        return file_name,path_sql_parquet

