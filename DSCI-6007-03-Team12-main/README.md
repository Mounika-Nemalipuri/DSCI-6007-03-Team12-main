**Remote Patient Care: Health Monitoring and Adherence with AWS and IoT**				

**Overview**

This project aims to monitor the health of patients using AWS IoT, data transformation with AWS Glue, machine learning models deployed on EC2, and a web application to display health status.
The workflow includes:
1.	Data ingestion from IoT devices.
2.	ETL (Extract, Transform, Load) using AWS Glue.
3.	Machine learning-based health monitoring on EC2.
4.	Displaying results via a web application.

**Architecture**

**Components**
1.	IoT Devices: Devices sending patient health data to AWS IoT Core.
2.	S3 Buckets:
 - Raw Data Bucket: Stores raw data in CSV format from IoT devices.
 - Transformed Data Bucket: Stores transformed data after ETL operations.
3.	AWS Glue: Handles ETL operations to transform raw data into structured format.
4.	EC2 Instance: Hosts machine learning models for patient health monitoring.
5.	Web Application: Displays patient health status based on ML model predictions.

**Setup Instructions**
1. IoT Setup:		   																																																																																																
 - Register IoT devices with AWS IoT Core.		
 - Configure IoT devices to send data to AWS IoT.
2. S3 Bucket Setup:                                                        				
 - Create S3 buckets for raw and transformed data.		
 - Grant necessary permissions for Glue and EC2 to access these buckets.		
3. AWS Glue Setup:
 - Create Glue jobs for ETL operations.
 - Schedule jobs as needed for data transformation.
4. EC2 Setup:
 - Launch an EC2 instance with required specifications.
 - Install necessary dependencies (Python, ML libraries, etc.).
 - Deploy machine learning models for patient health monitoring.
5. Web Application Setup:
 - Develop a web application using suitable frameworks (Flask, Django, etc.).
 - Use AWS SDK or APIs to fetch data from S3 and EC2 for display.
6. Integration:
 - Ensure IoT devices are sending data to AWS IoT.
 - Verify Glue jobs are transforming data correctly.
 - Test machine learning models on EC2 for accuracy.
 - Integrate web application with EC2 for real-time updates.

