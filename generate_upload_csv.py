from Generation.generate_film.generate_films_author import generate_film
from Generation.generate_client.generate_client import generate_client
from Upload.upload_files_gcp import upload_blob


def generate_upload_csv(film_rows_number=1e5,client_rows_number=1e4) : 
    # Generation 
    film_file_name,path_film_csv = generate_film.generate_film_csvfile(film_rows_number)
    client_file_name,path_client_csv = generate_client.generate_client_csvfile(client_rows_number)

    # Upload
    bucket_name="movies-personal"
    print('--------------------------Connecting to GCP----------------------------')
    upload_blob(bucket_name=bucket_name,source_file_name=path_film_csv,destination_blob_name=film_file_name)
    upload_blob(bucket_name=bucket_name,source_file_name=path_client_csv,destination_blob_name=client_file_name)