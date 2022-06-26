terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "eu-west-1"
}

resource "aws_instance" "android_terminator" {

  count = 10

  ami             = "ami-0e0f48e669d76f99d"
  instance_type   = "t2.micro"
  security_groups = ["no-security-no-cry"]
  user_data       = "${file("go_${count.index}.sh")}"

  tags = {
    Name = "article-${count.index}"
  }
  volume_tags = {
    "Name" = "article-${count.index}"
  }
}