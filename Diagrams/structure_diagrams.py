from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.compute import Functions
from diagrams.gcp.migration import TransferAppliance
from diagrams.gcp.database import SQL
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS
from diagrams.gcp.ml import AIPlatform

    
import os 
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'


with Diagram("Generate, Retrieve and Process Data", show=False,outformat='png'):
    

    with Cluster("Data Genration and  Retrieval"):
        sdk = TransferAppliance("generate_upload.py")
        with Cluster("Source of Data"):
            [IotCore("Faker Generator")] >> sdk

            with Cluster("PostgreSQL"):
                flow = SQL("Retrieve Table") >> sdk
    
    with Cluster("Targets"):

        with Cluster("Bucket"):
            storage = GCS("storage") 
            BigQuery = BigQuery("BigQuery")
            

            with Cluster("Process Data"):
                functions = Functions("functions")
                Workflow = Functions("Workflow")
                
                functions >> Workflow
            storage >> functions  
            Workflow >> BigQuery 

        with Cluster("Processing"):
            BigQuery >> AIPlatform("Processing notebooks")

    sdk >> storage