import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node customer_curated
customer_curated_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_curated",
    transformation_ctx="customer_curated_node1",
)

# Script generated for node step_trainer_landing
step_trainer_landing_node1675075149034 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_landing",
    transformation_ctx="step_trainer_landing_node1675075149034",
)

# Script generated for node Join
customer_curated_node1DF = customer_curated_node1.toDF()
step_trainer_landing_node1675075149034DF = step_trainer_landing_node1675075149034.toDF()
Join_node2 = DynamicFrame.fromDF(
    customer_curated_node1DF.join(
        step_trainer_landing_node1675075149034DF,
        (
            customer_curated_node1DF["serialnumber"]
            == step_trainer_landing_node1675075149034DF["serialnumber"]
        ),
        "left",
    ),
    glueContext,
    "Join_node2",
)

# Script generated for node Drop Fields
DropFields_node1675075359202 = DropFields.apply(
    frame=Join_node2,
    paths=[
        "customername",
        "email",
        "phone",
        "birthday",
        "registrationdate",
        "lastupdatedate",
        "sharewithresearchasofdate",
        "sharewithpublicasofdate",
    ],
    transformation_ctx="DropFields_node1675075359202",
)

# Script generated for node step_trainer_trusted
step_trainer_trusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1675075359202,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lh/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="step_trainer_trusted_node3",
)

job.commit()
