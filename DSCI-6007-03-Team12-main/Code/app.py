from flask import Flask, render_template, request
import pandas as pd
import boto3
import json
import time
import os

app = Flask(__name__)

# AWS IoT Analytics client setup
iot_analytics_client = boto3.client('iotanalytics')

# Define your AWS IoT Analytics channel name
CHANNEL_NAME = 'channel'

# Temporary directory for file uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML template for file upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Upload CSV file and process/send data to IoT Analytics
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return render_template('upload.html', message='No file selected')

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

    # Process CSV file
    df = pd.read_csv(file_path)

    # Prepare messages for IoT Analytics
    messages = []
    for idx, record in enumerate(df.to_dict(orient='records')):
        message_id = f"{int(time.time())}_{idx}"  # Generate a timestamp-based messageId
        payload = record
        messages.append({'messageId': message_id, 'payload': json.dumps(payload)})

    # Split messages into smaller batches
    batch_size = 100  # Adjust batch size as needed
    message_batches = [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]

    # Send data to IoT Analytics in smaller batches
    for message_batch in message_batches:
        response = iot_analytics_client.batch_put_message(
            channelName=CHANNEL_NAME,
            messages=message_batch
        )

    return render_template('upload.html', message='File uploaded and data sent to IoT Analytics')

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=8000,debug=True)
