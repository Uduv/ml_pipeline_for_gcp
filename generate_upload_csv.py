from Generation.generate_film.generate_films_author import generate_film
from Generation.generate_client.generate_client import generate_client
from Upload.upload_files_gcp import upload_blob



if __name__ == "__main__" :
    # Generation 
    film_file_name,path_film_csv = generate_film.generate_film_csvfile(rows_number=5e6)
    client_file_name,path_client_csv = generate_client.generate_client_csvfile(rows_number=1e5)

    # Upload
    bucket_name="movies-personal"
    upload_blob(bucket_name=bucket_name,source_file_name=path_film_csv,destination_blob_name=film_file_name)
    upload_blob(bucket_name=bucket_name,source_file_name=path_client_csv,destination_blob_name=client_file_name)