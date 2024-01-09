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
Crear archivo provider.tf
```terraform
provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
}
```

Crear archivo provider.tf
```terraform
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
```

Ejecutar comandos
```shell
tflocal init
tflocal plan
tflocal apply -auto-approve
```
