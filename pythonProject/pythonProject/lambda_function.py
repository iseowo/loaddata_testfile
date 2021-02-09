import boto3
import urllib
import io
import os
import json
import logging
from datetime import datetime

now = datetime.now().strftime("%Y%m%d%H%M%S")
print('start', now)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def lambda_handler(event, context):
    global source_bucket
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    print('Souce key:', key)
    db_parm = ''
    username_parm = ''
    host_parm = ''

    schema = os.environ['targetSchema']
    domain = os.environ['DOMAIN']
    role = os.environ['ROLE']
    lockbox_id = os.environ['LOCKBOXID']
    auth_url = os.environ['AUTHURL']
    pw_parm = ''

    # print("Waiting for the file persist in the source bucket")
    waiter = s3.get_waiter('object_exists')
    waiter.wait(Bucket=source_bucket, Key=key)

    file_obj = s3.get_object(Bucket=source_bucket, Key=key)
    file_content = file_obj["Body"].read()
    read_csv_data = io.BytesIO(file_content)

    # Convert & Map datatype
    converted_dtype, date_columns = convert_datatype(key)
    print('converted_dtype:', converted_dtype)
    print('date_columns:', date_columns)

    # Retrieve Table Name
    table = key.split('_')[2]
    table = table.lower()
    table = 'bet_tb.' + table
    print('table_name', table)

    cv = daconn.DbConnection()
    conn, cur = cv.dbConnect(db_parm, username_parm, host_parm, pw_parm)

    df = pd.read_csv(read_csv_data, header=None, sep="|", dtype=converted_dtype, error_bad_lines=False, skiprows=1,
                     warn_bad_lines=True, low_memory=False).replace('"', '', regex=True)

    df = df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r", ","], value=["", "", " "], regex=True)

    df = df.fillna("")
    index = df.index
    number_of_rows = len(index)
    logger.info(number_of_rows)

    '''
    #call copy function
    copy_from_stringio(conn, df, table)
    print("Lambda Request ID:", context.aws_request_id , table)
    '''

    # Call funtion to load data to database
    # loaddb = daconn.DbConnection()
    cv.copy_from_stringio(conn, df, table)


def convert_datatype(key):
    tblName = key.split('/')[1].split('_')[2].lower()
    print('tblName', tblName)
    schemaFileObj = s3.get_object(Bucket=source_bucket, Key='BetODSProject/schemas/BET_Table_Schema.json')
    schema_file = json.loads(schemaFileObj['Body'].read())

    converted_dtype = schema_file[tblName]['Columns']

    date_columns = schema_file[tblName]['date_columns']
    date_columns = date_columns.split(",")
    return converted_dtype, date_columns
