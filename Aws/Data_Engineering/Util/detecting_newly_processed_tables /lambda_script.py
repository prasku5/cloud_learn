import boto3

s3 = boto3.client('s3')

def detect_new_tables(raw_bucket):
    # Assume we have a list of existing processed tables from a metadata store
    existing_tables = set(["table1", "table2", "table3"])
    
    # List all files/tables in the raw S3 bucket
    new_tables = set()
    response = s3.list_objects_v2(Bucket=raw_bucket, Prefix="raw/")

    for obj in response.get('Contents', []):
        table_name = obj['Key'].split('/')[1]  # Assuming structure: raw/table_name/file
        if table_name not in existing_tables:
            new_tables.add(table_name)

    return new_tables

# Detect new tables and write them to `tables_list.txt`
new_tables = detect_new_tables('raw-data-bucket')
with open('tables_list.txt', 'w') as f:
    for table in new_tables:
        f.write(f"{table}\n")
