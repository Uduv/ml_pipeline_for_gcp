from google.cloud import storage
import os


def upload_blob(bucket_name="movies-personal" , source_file_name="Generation\data\client\DATASET.csv", destination_blob_name="FILENAME_ON_GCP.csv"):
    """Uploads a file to the bucket.
    The ID of your GCS \n
    bucket_name = "your-bucket-name" \n
    The path to your file to upload \n
    source_file_name = "local/path/to/file" \n
    The ID of your GCS object \n
    destination_blob_name = "storage-object-name"
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try : 
        blob.upload_from_filename(source_file_name)
    except Exception as e:
        print('You may disconnect yourself to the VPN')
        print(e)
        exit()
        
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


# Exemple of parameters
bucket_name = "movies-personal" 
source_file_name = "Generation\data\client\client_1000000.0_rows_17h53m54s.csv"
destination_blob_name = "client_remote.csv"
os.environ["GCLOUD_PROJECT"] = "ID_PROJECT"

if __name__ == '__main__' :
    
    upload_blob(bucket_name, source_file_name, destination_blob_name)

