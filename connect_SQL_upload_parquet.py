from Generation.generate_client.generate_client import generate_client
from Data_PostgreSQL.connect_to_postgreSQL import postgreSQL 
from Upload.upload_files_gcp import upload_blob



if __name__ == "__main__" :
    # Generation 
    file_name,path_sql_parquet = postgreSQL.generate_postgreSQL_parquet()

    # Upload
    bucket_name="movies-personal"
    upload_blob(bucket_name=bucket_name,source_file_name=path_sql_parquet,destination_blob_name=file_name)