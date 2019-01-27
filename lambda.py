import json
import boto3
import time


def lambda_handler(event, context):
    # TODO implement
   
    ec2 = boto3.resource('ec2')
    
    ids = #[''] id of EC2 instance.
    status = ec2.instances.filter(InstanceIds=ids).stop()
    
    
    client = boto3.client('ec2')
    rsp = client.describe_instances(InstanceIds=ids)
    status = rsp['Reservations'][0]['Instances'][0]['State']['Name']
    
    while status != 'stopped':
        time.sleep(10)
        
        rsp = client.describe_instances(InstanceIds=ids)
        status = rsp['Reservations'][0]['Instances'][0]['State']['Name']
    
    status = ec2.instances.filter(InstanceIds=ids).start()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
