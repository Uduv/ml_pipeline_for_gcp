from connect_SQL_upload_parquet import connect_SQL_upload_parquet
from generate_upload_csv import generate_upload_csv


if __name__ == "__main__" :
    for x in range(30):
        generate_upload_csv(10,10)