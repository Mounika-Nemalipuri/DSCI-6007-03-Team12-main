import boto3
from io import StringIO
import pandas as pd

# Create an S3 client
s3_client = boto3.client('s3')

# Read CSV file from S3
try:
    response = s3_client.get_object(Bucket='waste1', Key='patient_data.csv')
    csv_data = response['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_data))
    print(df)  # Display the contents of the CSV file as a pandas DataFrame
except Exception as e:
    print(f"Error reading CSV file from S3: {e}")
