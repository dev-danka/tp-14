import boto3
import time

# Configuración de LocalStack
localstack_endpoint = 'http://localhost.localstack.cloud:4566'
aws_access_key_id = "test"
aws_secret_access_key = "test"
aws_region = "us-east-1"

# Crear una tabla en DynamoDB en LocalStack
def create_dynamodb_table():
    dynamodb = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region, endpoint_url=f'{localstack_endpoint}/dynamodb')

    table_name = 'tabla-de-prueba'
    attribute_definitions = [{'AttributeName': 'ID', 'AttributeType': 'N'}]
    key_schema = [{'AttributeName': 'ID', 'KeyType': 'HASH'}]
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}

    response = dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        ProvisionedThroughput=provisioned_throughput
    )

    print(f'Tabla DynamoDB creada en LocalStack: {response["TableDescription"]["TableName"]}')

# Crear una cola en SQS en LocalStack
def create_sqs_queue():
    sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region, endpoint_url=f'{localstack_endpoint}/sqs')

    queue_name = 'queue-one-py'
    response = sqs.create_queue(QueueName=queue_name)

    print(f'Cola SQS creada en LocalStack: {response["QueueUrl"]}')

# Lanzar una instancia EC2 en LocalStack
def launch_ec2_instance():
    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region, endpoint_url=f'{localstack_endpoint}/ec2')

    ami_id = 'ami-ff0fea8310f3'  # Reemplaza con un AMI válido
    instance_type = 't3.nano'

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f'Instancia EC2 lanzada en LocalStack: {instance_id}')

# Llamar a las funciones para crear los recursos en LocalStack
create_dynamodb_table()
create_sqs_queue()
launch_ec2_instance()



