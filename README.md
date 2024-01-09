# Levantar localmente 2 ec2 de aws con localstack

## Instalacion de localstack

Crear virtual env
´´´
python3 -m venv ./venv
#Activar el entorno
source ./venv/bin/activate
´´´

Instalar dentro del env localstack, el cli de aws y el local aws
´´´
python3 -m pip install --upgrade localstack
pip install awscli
pip install awscli-local
pip install terraform-local
´´´

Configurar las variables
´´´
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

#Testear
aws --endpoint-url=http://localhost:4566 kinesis list-streams
´´´

## Creando las ec2

Crear un archivo llamado user_script.sh con este contenido
´´´
#!/bin/bash -xeu

apt update
apt install python3 -y
python3 -m http.server 8000
´´´

Pasos para levantar las ec2
´´´
awslocal ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text | tee key.pem

chmod 400 key.pem

awslocal ec2 authorize-security-group-ingress \
    --group-id default \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0
´´´

De este comando debemos extraer el GroupId
´´´
awslocal ec2 describe-security-groups
´´´

Y luego ese id pasarlo al parametro security-group-id
´´´
awslocal ec2 run-instances \
    --image-id ami-ff0fea8310f3 \
    --count 2 \
    --instance-type t3.nano \
    --key-name my-key \
    --security-group-ids 'colocar el security group id' \
    --user-data file://./user_script.sh
´´´


## Con terraform
Crear archivo provider.tf
´´´
provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
}
´´´

Crear archivo provider.tf
´´´
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-ff0fea8310f3"
  instance_type = "t3.nano"

  tags = {
    Name = "ExampleAppServerInstance"
  }
  count = 2
}
´´´

Ejecutar comandos
´´´
tflocal init
tflocal plan
tflocal apply
´´´
