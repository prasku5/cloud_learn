import os

def generate_glue_script(table_name, script_s3_bucket):
    script_template = f"""
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name'])

# Glue/Spark setup
glueContext = GlueContext(SparkContext.getOrCreate())
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load the raw data from S3
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database="raw_database",
    table_name=args['table_name']
)

# Transformation logic (add your business logic here)

# Write to the staging layer
output_path = f"s3://target-bucket/staging/{args['table_name']}"
raw_data.toDF().write.mode("overwrite").parquet(output_path)

job.commit()
"""
    script_path = f"/tmp/{table_name}_etl_script.py"
    
    with open(script_path, 'w') as f:
        f.write(script_template)
    
    # Upload to S3
    os.system(f"aws s3 cp {script_path} s3://{script_s3_bucket}/scripts/")

# Read list of new tables
with open('tables_list.txt', 'r') as f:
    tables = [line.strip() for line in f.readlines()]

# Generate Glue scripts for each table
for table_name in tables:
    generate_glue_script(table_name, 'scripts-bucket')
