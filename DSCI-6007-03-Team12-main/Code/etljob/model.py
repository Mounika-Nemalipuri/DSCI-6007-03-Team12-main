from flask import Flask, render_template
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from joblib import dump
import boto3
from io import StringIO
from io import BytesIO

#heart
heartdf = pd.read_csv(r"Heart/heart.csv")
heartdf.head(3)

#print(heartdf.info(), heartdf.isnull().sum())

x_df = heartdf.drop(columns=['Target'])
y_df = heartdf['Target']

x_train ,x_test, y_train , y_test = train_test_split(x_df,y_df,test_size=0.2,random_state=45 )

rf_heart = RandomForestClassifier(random_state=42)
rf_heart.fit(x_train, y_train)

rf_pred = rf_heart.predict(x_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
#print("Accuracy of Random Forest:", rf_accuracy)

#diabetics
diadf = pd.read_csv(r"Diabetics/diabetics.csv")
diadf.head(3)

#print(diadf.info(), diadf.isnull().sum())

x_df = diadf.drop(columns=['Target'])
y_df = diadf['Target']

x_train ,x_test, y_train , y_test = train_test_split(x_df,y_df,test_size=0.2,random_state=45 )

rf_dia = RandomForestClassifier(random_state=42)
rf_dia.fit(x_train, y_train)

rf_pred = rf_dia.predict(x_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
#print('Accuracy of Random Forest {:.2f}'.format(rf_accuracy))



#Dementia 
demdf = pd.read_csv(r"Dementia/dementia.csv")
demdf.head(3)
#print(demdf.info(), demdf.isnull().sum())
demdf['prescription'].fillna('No', inplace=True)
demdf['dosage in mg'].fillna(0,inplace=True)
demdf['chronic_health_conditions'].fillna('Good',inplace =True)

for column in demdf.columns:
    if demdf[column].dtype == type(object):
        le = sklearn.preprocessing.LabelEncoder()
        demdf[column] = le.fit_transform(demdf[column])
x = demdf.drop(columns=['Target'])

y = demdf['Target']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForestClassifier
rf_dem = RandomForestClassifier(n_estimators=100, random_state=42)
rf_dem.fit(X_train, y_train)

# Making predictions
y_pred = rf_dem.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
#print("Accuracy:", accuracy)

# Classification report
#print(classification_report(y_test, y_pred))

s3_client = boto3.client('s3')
#s3://waste1/output1/part-00000-f0d6cfad-d5fc-412f-8ee4-3db5312e05ab-c000.csv
# Read CSV file from S3
try:
    response = s3_client.get_object(Bucket='waste1', Key='output1/part-00000-f0d6cfad-d5fc-412f-8ee4-3db5312e05ab-c000.csv')
    csv_data = response['Body'].read().decode('utf-8')
    datacollected = pd.read_csv(StringIO(csv_data))
    #print(datacollected)  # Display the contents of the CSV file as a pandas DataFrame
except Exception as e:
    print(f"Error reading CSV file from S3: {e}")


#print(heartdf.columns,diadf.columns, demdf.columns )

v1=[col for col in heartdf.columns if col != 'Target']
v2=[col for col in diadf.columns if col != 'Target']
v3=[col for col in demdf.columns if col != 'Target']

#print(v1,datacollected.columns)
datacollected['sex']=[0 if i =='Female' else 1 for i in datacollected['gender']]
ctoutput1 = rf_dia.predict(datacollected[v2])
datacollected['diabetic'] = ctoutput1
#print(datacollected['diabetic'])
datacollected['BMI']=datacollected['weight']/(datacollected['height']*datacollected['height'])

ctoutput2 = rf_heart.predict(datacollected[v1])

#datacollected['Chronic_Health_Conditions'] = ['Diabetes' if i else 'No' for i in ctoutput1]
#datacollected['Chronic_Health_Conditions'] = ['Heart Disease' if i else 'No' for i in ctoutput2]
#datacollected[(datacollected['Chronic_Health_Conditions']=='N0') & ctoutput1]['Chronic_Health_Conditions']  = 'Diabetes'
#print(datacollected['Chronic_Health_Conditions'])

#ctoutput3 = rf_dem.predict(datacollected[v3])

#datacollected['Dementia'] = ['No' if i else 'Yes' for i in ctoutput3]

datacollected['chronic_health_conditions'] = ['Diabetes' if i else 'No' for i in ctoutput1]
datacollected['chronic_health_conditions'] = ['Heart Disease' if i else 'No' for i in ctoutput2]

# Set 'Chronic_Health_Conditions' based on conditions from ctoutput1 and ctoutput2
datacollected.loc[(datacollected['chronic_health_conditions'] == 'No') & ctoutput1, 'chronic_health_conditions'] = 'Diabetes'
datacollected.loc[(datacollected['chronic_health_conditions'] == 'No') & ctoutput2, 'chronic_health_conditions'] = 'Heart Disease'

#print(datacollected['chronic_health_conditions'])
#print(datacollected.columns)

datacollected['physical_activity'] =datacollected['physactivity']
datacollected['apoe'] =datacollected['apoe_ε4']

for column in datacollected.columns:
    if datacollected[column].dtype == type(object) and (column not in ['patient_name','patient_id']):
        le = sklearn.preprocessing.LabelEncoder()
        datacollected[column] = le.fit_transform(datacollected[column])

ctoutput3 = rf_dem.predict(datacollected[v3])
datacollected['Dementia'] = ['No' if i else 'Yes' for i in ctoutput3]
datacollected['Heart'] = ['Bad' if i else 'Good' for i in ctoutput2]
datacollected['Suger_level'] = ['Bad' if i else 'Good' for i in ctoutput1]
datacollected['chronic_health_conditions'] = ['Diabetes' if i else 'No' for i in ctoutput1]
datacollected['chronic_health_conditions'] = ['Heart Disease' if i else 'No' for i in ctoutput2]

# Set 'Chronic_Health_Conditions' based on conditions from ctoutput1 and ctoutput2
datacollected.loc[(datacollected['chronic_health_conditions'] == 'No') & ctoutput1, 'chronic_health_conditions'] = 'Diabetes'
datacollected.loc[(datacollected['chronic_health_conditions'] == 'No') & ctoutput2, 'chronic_health_conditions'] = 'Heart Disease'



outputdf =  pd.DataFrame(datacollected[['patient_name','patient_id','Heart','Suger_level','Dementia','chronic_health_conditions']])

csv_buffer = BytesIO()
outputdf.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)
s3_client.put_object(Bucket='bucket-dataset1', Key='Doctor_view.csv', Body=csv_buffer.getvalue())




# Assume 'outputdf' is already defined and has data

app = Flask(__name__)

@app.route('/')
def display_dataframe():
    # Render the 'outputdf' DataFrame as an HTML table
    return render_template('index.html', tables=[outputdf.to_html(classes='data')], titles=outputdf.columns.values)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
