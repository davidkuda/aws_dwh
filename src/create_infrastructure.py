from aws_client.aws_client import get_aws_instance, create_infrastructure

if __name__ == '__main__':
    aws = get_aws_instance()
    create_infrastructure(aws)
