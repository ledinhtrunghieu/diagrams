# make sure the Graphviz executables are on your systems' path
import os
os.environ["PATH"] += os.pathsep + 'D:/Graphviz/bin/'


from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import Users

from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3



with Diagram(name="Data Diagrams", show=True):
    localdev = Client('Local Dev')
    docker = Docker('Docker')
    users = Users('Users/Data Consumers')
    with Cluster("Airflow control plane"):
        airflow = Airflow('Airflow')
        with Cluster("Local On Premises"):
            with Cluster("Event Workers"):
                workers = [ECS("worker1"),
                        ECS("worker2"),
                        ECS("worker3")]

            queue = SQS("event queue")

            with Cluster("Processing"):
                handlers = [Lambda("proc1"),
                            Lambda("proc2"),
                            Lambda("proc3")]


        with Cluster("AWS Cloud"):
            with Cluster("Event Workers 2"):
                workers2 = [ECS("worker1"),
                        ECS("worker2"),
                        ECS("worker3")]

            queue2 = SQS("event queue")

            with Cluster("Processing 2 "):
                handlers2 = [Lambda("proc1"),
                            Lambda("proc2"),
                            Lambda("proc3")]

        store = S3("events store")

    localdev >> docker >> airflow
    airflow >> workers >> queue >> handlers
    airflow >> workers2 >> queue2 >> handlers2
    handlers >> store
    handlers2 >> store
    store >> users
