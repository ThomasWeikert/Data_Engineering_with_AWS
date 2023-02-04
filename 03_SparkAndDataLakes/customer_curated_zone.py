import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer trusted
Customertrusted_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_trusted",
    transformation_ctx="Customertrusted_node1",
)

# Script generated for node Accelerometer landing
Accelerometerlanding_node1675075149034 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerator_landing",
    transformation_ctx="Accelerometerlanding_node1675075149034",
)

# Script generated for node Join
Join_node2 = Join.apply(
    frame1=Customertrusted_node1,
    frame2=Accelerometerlanding_node1675075149034,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="Join_node2",
)

# Script generated for node Drop Fields
DropFields_node1675075359202 = DropFields.apply(
    frame=Join_node2,
    paths=["user", "timestamp", "x", "y", "z"],
    transformation_ctx="DropFields_node1675075359202",
)

# Script generated for node Customer_curated
Customer_curated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1675075359202,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-lh/customer/curated/", "partitionKeys": []},
    transformation_ctx="Customer_curated_node3",
)

job.commit()
