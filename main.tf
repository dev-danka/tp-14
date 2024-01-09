terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_security_group" "my_security_group" {
  name        = "my-security-group"
  description = "Security group for my EC2 instances"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-ff0fea8310f3"
  instance_type = "t3.nano"
  vpc_security_group_ids  = [aws_security_group.my_security_group.id]
  user_data       = file("user_script.sh")

  tags = {
    Name = "ExampleAppServerInstance"
  }
  count = 2
}