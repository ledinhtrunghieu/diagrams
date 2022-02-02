# make sure the Graphviz executables are on your systems' path
import os
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
from diagrams.onprem.analytics import Metabase
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.onprem.queue import Kafka
from diagrams.aws.analytics import Kinesis





with Diagram(name="Data Diagrams", show=True, direction="LR"):
    localdev = Client('Local Dev')
    docker = Docker('Docker')
    users = Users('Users/Data Consumers')

    with Cluster("Airflow control plane"):
        airflow = Airflow('Airflow')

        with Cluster("Local On Premises"):
            local_rawdata = Datacenter("Raw Data")

            with Cluster("Data Warehouse"):
                dw_local_clean = Python("Pandas")
                with Cluster("Column-Oriented Wrappers"):
                    dw_local_postgresql = Postgresql('Postgre SQL')
                local_rawdata >> dw_local_clean >> dw_local_postgresql

            with Cluster("Data Lake"):
                dw_local_spark = Spark("Spark")
                dw_local_storage = Storage("Storage")
                local_rawdata >> dw_local_spark >> dw_local_storage >> dw_local_postgresql

        with Cluster("AWS Cloud"):
            cloud_s3 = S3("Amazon S3")

            with Cluster("Data Warehouse"):
                cloud_ec2 = EC2("AWS EC2") 
                cloud_redshift = Redshift('AWS Redshift')
                cloud_s3 >> cloud_ec2 >> cloud_redshift

            with Cluster("Data Lake"):
                cloud_emr= EMR('AWS EMR')
                cloud_bucket = S3("S3 Buckets")
                cloud_s3 >> cloud_emr >> cloud_bucket >> cloud_redshift

        metabase =  Metabase("Metabase")
        cloud_alb = ElbApplicationLoadBalancer("Application Load Balancer")


    
    localdev >> docker >> airflow
    airflow >> cloud_s3
    airflow >> local_rawdata
    cloud_bucket >> metabase
    cloud_redshift >> metabase
    dw_local_storage >> metabase
    dw_local_postgresql >> metabase
    metabase >> cloud_alb >> users
