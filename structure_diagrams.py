from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions,GPU
from diagrams.gcp.migration import TransferAppliance
from diagrams.gcp.database import BigTable,SQL
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS
from diagrams.gcp.devtools import SDK
from diagrams.gcp.ml import AIPlatform

    
import os 
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'


with Diagram("Generate and Process Data", show=False):
    

    with Cluster("On-Prem"):
        sdk = TransferAppliance("generate_upload.py")
        with Cluster("Source of Data"):
            [IotCore("Faker Generator")] >> sdk

            with Cluster("PostgreSQL"):
                flow = SQL("Retrieve Table") >> sdk
    
    with Cluster("Targets"):

        with Cluster("Data Lake"):
            storage = GCS("storage") 
            BigQuery = BigQuery("BigQuery")
            storage >> BigQuery

        with Cluster("Event Driven"):
            with Cluster("Processing"):
                BigQuery >> AIPlatform("Processing notebooks")

    sdk >> storage