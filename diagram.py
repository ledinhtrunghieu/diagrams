# make sure the Graphviz executables are on your systems' path
import os

from flask_login import AUTH_HEADER_NAME
os.environ["PATH"] += os.pathsep + 'D:/Graphviz/bin/'


from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import Users
from diagrams.generic.place import Datacenter
from diagrams.programming.language import Python
from diagrams.onprem.database import Postgresql
from diagrams.onprem.analytics import Spark
from diagrams.generic.storage import Storage
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR
from diagrams.aws.compute import EC2
from diagrams.aws.database import Redshift
from diagrams.onprem.analytics import Superset
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.onprem.queue import Kafka
from diagrams.aws.analytics import Kinesis
from diagrams.onprem.analytics import Dbt
from diagrams.custom import Custom

with Diagram(name="Data Diagrams", show=True, direction="LR"):
    localdev = Client('Local Dev')
    docker = Docker('Docker')
    users = Users('Users/Data Consumers')

    with Cluster("Airflow control plane"):
        airflow = Airflow('Airflow')

        with Cluster("Local On Premises"):
            local_rawdata = Datacenter("Raw Data")

            with Cluster("Data Warehouse"):
                dw_local_dbt = Dbt("Transform")
                local_ge = Custom("greate_expectations","./custom_icons/ge.png")
                with Cluster("Column-Oriented Wrappers"):
                    dw_local_postgresql = Postgresql('Postgre SQL')

            with Cluster("Data Lake"):
                dw_local_spark = Spark("Spark")
                local_df = Python("DataFrame")
                local_dl = Custom("File Format","./custom_icons/dl.png")
                dw_local_storage = Storage("Storage")
                local_rawdata >> local_df >> dw_local_spark >> local_dl >> dw_local_storage >> dw_local_dbt >> local_ge >> dw_local_postgresql
                local_jp = Custom("File Format","./custom_icons/dl.png")
            superset1 =  Superset("Local Dashboard")
        
        with Cluster("AWS Cloud"):
            cloud_ec2 = EC2("AWS EC2")

            with Cluster("Data Warehouse"):
                cloud_dbt = Dbt("Transform") 
                cloud_ge = Custom("greate_expectations","./custom_icons/ge.png")
                cloud_redshift = Redshift('AWS Redshift')

            cloud_s3 = S3("S3 Buckets")

            with Cluster("Data Lake"):
                cloud_emr= EMR('AWS EMR')
                cloud_dl = Custom("File Format","./custom_icons/dl.png")
                cloud_bucket = S3("Data Lake")
                cloud_ec2 >> cloud_s3 >> cloud_emr >> cloud_dl >> cloud_bucket >> cloud_dbt >> cloud_ge >> cloud_redshift

            cloud_alb = ElbApplicationLoadBalancer("Application Load Balancer")
            
            superset2 =  Superset("Cloud Dashboard")
        
       

    
    localdev >> docker >> airflow
    airflow >> cloud_ec2 
    airflow >> local_rawdata
    cloud_redshift >> cloud_alb
    dw_local_postgresql >> superset1 >> users
    cloud_alb >> superset2 >> users
    
Jupyter 
Athena
DataHub
Synthea
