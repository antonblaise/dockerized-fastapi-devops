terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "ap-southeast-1"
}

resource "aws_instance" "fastapi-server" {
    ami = "ami-02dd44faa40720bb8"
    instance_type = "t3.micro"

    tags = {
        Name = "fastapi-dev-server"
    }

    key_name = "fastapi-dev-key"

    vpc_security_group_ids = [aws_security_group.fastapi-sg.id]
}

resource "aws_security_group" "fastapi-sg" {
    name = "fastapi-security-group"

    ingress {
        description = "SSH"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "FastAPI"
        from_port = 8000
        to_port = 8000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "fastapi-security-group"
    }
}