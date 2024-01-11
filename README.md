# Levantar localmente 2 ec2 de aws con localstack

## Instalacion de localstack

Crear virtual env
```shell
python3 -m venv ./venv
#Activar el entorno
source ./venv/bin/activate
```

Instalar dentro del env localstack, el cli de aws y el local aws
```shell
python3 -m pip install --upgrade localstack
pip install awscli awscli-local terraform-local
```

Configurar las variables
```shell
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

#Iniciar el stack
localstack start

#Testear
awslocal kinesis list-streams
```

## Creando las ec2

Crear un archivo llamado user_script.sh con este contenido
```shell
touch user_script.sh

nano user_script.sh

#!/bin/bash -xeu

apt update
apt install python3 -y
python3 -m http.server 8000
```

Pasos para levantar las ec2
```shell
awslocal ec2 authorize-security-group-ingress \
    --group-id default \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0
```

De este comando debemos extraer el GroupId
```shell
awslocal ec2 describe-security-groups
```

Y luego ese id pasarlo al parametro security-group-id colocar el security group id
```shell
awslocal ec2 run-instances \
    --image-id ami-ff0fea8310f3 \
    --count 2 \
    --instance-type t3.nano \
    --security-group-ids 'sg-ba212ac91e4d91d7e' \
    --user-data file://./user_script.sh  
```

Chequear que estan ejecutandose
```shell
awslocal ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,PublicIpAddress,State.Name]' --output table
```

## Con terraform
Crear archivo provider.tf y main.tf

Ejecutar comandos
```shell
tflocal init
tflocal plan
tflocal apply -auto-approve
```

localstack logs
be accessible via SSH at: 127.0.0.1:12862, 172.17.0.4:22
curl 172.17.0.4:8000


## Creando las SQS
Se agrego al main.tf el codigo:

```terraform
resource "aws_sqs_queue" "tf_queue_one" {
  name                      = "queue-one"
  delay_seconds             = 10
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "production"
  }
}

resource "aws_sqs_queue" "tf_queue_two" {
  name                      = "queue-two"
  delay_seconds             = 10
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "production"
  }
}
```

Ejecutar comandos de terraform
```shell
tflocal plan
tflocal apply -auto-approve
```

Para probar usamos el envio de mensajes
```shell
awslocal sqs send-message \
    --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-one \
    --message-body "Prueba a sqs 1.0"

awslocal sqs send-message \
    --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-one \
    --message-body "Prueba a sqs 1.1"

awslocal sqs send-message \
    --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-two \
    --message-body "Prueba a sqs 2.0"   

awslocal sqs send-message \
    --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-two \
    --message-body "Prueba a sqs 2.1"    
```   

Para recepcionar los mensajes
```shell
awslocal sqs receive-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-one

awslocal sqs receive-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-one

awslocal sqs receive-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-two

awslocal sqs receive-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/queue-two
```

## Creando la DynamoDB
Se agrego al main.tf el codigo:

```terraform
resource "aws_dynamodb_table" "primera_tabla" {
  name           = "PrimeraTabla"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "Id"

  attribute {
    name = "Id"
    type = "S"
  }
}
```

Ejecutar comandos de terraform
```shell
tflocal plan
tflocal apply -auto-approve
```


## Creando todo con python
Ejecutar el archivo de python 
```python
python3 scrypt.py
```