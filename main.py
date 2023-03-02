from connect_SQL_upload_parquet import connect_SQL_upload_parquet
from generate_upload_csv import generate_upload_csv


if __name__ == "__main__" :
    # call retrieve from PostGreSQL and upload to GCP
    connect_SQL_upload_parquet()
    # Call generation and upload to GCP
    generate_upload_csv()