import boto3

def lambda_handler(event, context):
    # Initialize AWS IoT Analytics client
    iot_analytics = boto3.client('iotanalytics')

    # Specify the name of your IoT Analytics pipeline
    pipeline_name = 'streampipeline'

    # Start the pipeline execution
    response = iot_analytics.start_pipeline_reprocessing(
        pipelineName=pipeline_name
    )

    # Print the response for logging or monitoring
    print(response)

    # Optionally, you can handle errors and add additional logic here
