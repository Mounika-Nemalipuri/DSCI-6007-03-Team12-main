from flask import Flask, render_template, request, redirect, url_for , session
import boto3
import csv
from io import StringIO
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy user credentials (replace with your actual authentication logic)

s3 = boto3.client('s3')

username = 'no'

# AWS credentials and region
s3_client = boto3.client('s3')

try:
    response = s3_client.get_object(Bucket='waste1', Key='patient_data.csv')
    csv_data = response['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_data))
     #   response= s3.get_object(Bucket='waste1',key='patient_data.csv')
     #   content = response['Body'].read().decode('utf-8')
     #   userk = json.loads(content)
     #   print(userk)
except Exception as e:
    print(f'Error reading the file fom S3 {e}')


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username in df['patient_id']) and (password in df['patient_name']):
            # Successful login, redirect to the index page
            return redirect(url_for('details'))  
        else:
            # Failed login, redirect back to login page with a message
            return render_template('index.html', message='Invalid credentials. Please try again.')

    return render_template('index.html')


@app.route('/details', methods=['GET','POST'])
def details():
 if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username

        if (int(username) in df['patient_id'].values) and (password in df['patient_name'].values):
            username = session['username']
            return render_template('details.html', username=username)
    #return render_template('details.html')

        else:
             return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    # Get data from the form
    patient_name = request.form['patient_name']
    weight = request.form['weight']
    smoking_status = request.form['smoking_status']
    depression_status = request.form['depression_status']
    Nutrition_Diet = request.form['Nutrition_Diet']
    cp =  request.form['cp']
    sleepq =  request.form['sleepq']
    user = session['username']

    # Process and store the data as needed (e.g., in a database)
    # In this example, we'll just append the data to a CSV file on S3

    # Get the existing CSV data from S3
    existing_csv_obj = s3_client.get_object(Bucket='bucket-dataset1', Key='data.csv')
    existing_csv_data = existing_csv_obj['Body'].read().decode('utf-8')

    # Parse the CSV data
    csv_data = StringIO(existing_csv_data)
    csv_reader = csv.reader(csv_data)
    rows = list(csv_reader)

    # Create a new row with the submitted data
    new_row = [ user, patient_name, weight, smoking_status, depression_status, Nutrition_Diet, cp, sleepq]
    rows.append(new_row)

    # Prepare updated CSV data
    updated_csv_data = StringIO()
    csv_writer = csv.writer(updated_csv_data)
    csv_writer.writerows(rows)

    # Upload updated CSV data to S3
    s3_client.put_object(Bucket='bucket-dataset1', Key='data.csv', Body=updated_csv_data.getvalue())

    return f"<h2>Details submitted successfully!</h2><p>Name: {patient_name}</p><p>Weight: {weight}</p><p>Smoking Status: {smoking_status}</p><p>Depression Status: {depression_status}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
