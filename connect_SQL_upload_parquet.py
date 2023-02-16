from Generation.generate_client.generate_client import generate_client
from Data_PostgreSQL.connect_to_postgreSQL import postgreSQL 
from Upload.upload_files_gcp import upload_blob



def connect_SQL_upload_parquet() :
    """Connect to PostgreSQL database and generate a parquet file for the given dataset

        Returns:
            string file_name : file name
            string path_sql_parquet : path to parquet file
        """ 
    print('--------------------------Connecting to the PostGreSQL database----------------------------')
    file_name,path_sql_parquet = postgreSQL.generate_postgreSQL_parquet()
    # Upload
    print('--------------------------Connecting to GCP----------------------------')
    bucket_name="movies-personal"
    upload_blob(bucket_name=bucket_name,source_file_name=path_sql_parquet,destination_blob_name=file_name)