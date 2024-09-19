import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

# Get table name and target layer from arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name', 'target_layer'])

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load raw table from S3
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database="raw_database",
    table_name=args['table_name']
)

# Apply some transformation logic (e.g., cleaning, deduplication)
transformed_data = raw_data.toDF().dropDuplicates()

# Perform SCD Type 2 logic, etc.
# Apply transformations according to your business rules...

# Write back to the target layer (staging or final)
transformed_data.write.mode("overwrite").parquet(f"s3://target_bucket/{args['target_layer']}/{args['table_name']}")

job.commit()
