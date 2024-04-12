import os
import io
import boto3
import json
import csv
import logging

# It is good practice to use proper logging.
# Here we are using the logging module of python.
# https://docs.python.org/3/library/logging.html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Endpoint name from the Environment variable
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

##When testing for island friendly vehicles uncomment these lines
value_0 = "No Special Event - Normal Crowds"
value_1 = "Special Event - Expect Crowds"


def lambda_handler(event, context):
  
   # Using sagemaker boto3 client.
   # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html
   sagemaker_runtime = boto3.client('sagemaker-runtime')
   
   # Reading the data payload from the test event
   data = json.loads(json.dumps(event))

   results = []

   for i in range(0,len(data)):
      payload = data['data'+str(i)]
      print(payload)
   
      # Sending the payload to the Sagemaker Endpoint using Invoke Endpoint API
      # Boto3 info: https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
   
      endpointresponse = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='text/csv',
            Body=payload
      )
   
      logger.info(endpointresponse)
      anomaly_score = json.loads(endpointresponse['Body'].read().decode())["scores"][0]["score"]
   
      if anomaly_score > 3:
         results.append("score: " + str(anomaly_score) + " " + value_1)
      else:
         results.append("score: " + str(anomaly_score) + " " + value_0)
       
   return results
   
   
"""

You can use the code below to create a test event called
CrowdEvents The below test represents the number of citizens walking in the last 2 hours and 
whether the number of citizens walking justifies an anomaly and adjust rental pricing accordingly.

{
  "data0": "22258",
  "data1": "12081",
  "data2": "37000",
  "data3": "38232"
}


"""