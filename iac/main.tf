provider "aws" {
  region = "eu-north-1"
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-04e4606740c9c9381"
  instance_type = "t3.micro"

  key_name      = "key_pair_echo_service"


  vpc_security_group_ids = ["sg-03297660ac1cd8560"]


  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y docker
              sudo service docker start
              sudo systemctl enable docker
              sudo usermod -a -G docker ec2-user
              docker --version
              $(aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 445673445791.dkr.ecr.eu-north-1.amazonaws.com)
              sudo docker pull 445673445791.dkr.ecr.eu-north-1.amazonaws.com/echo_service:latest
              sudo docker run -d -p 8000:8000 --name echo_service \
              -e ECHO_SERVICE_HOST=0.0.0.0 \
              -e ECHO_SERVICE_DB_FILE=/db_data/db.sqlite3 \
              -v echo_service-db-data:/db_data/ \
              445673445791.dkr.ecr.eu-north-1.amazonaws.com/echo_service:latest
              EOF
}
