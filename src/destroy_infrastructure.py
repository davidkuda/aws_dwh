from aws_client.aws_client import get_aws_instance, destroy_infrastructure

if __name__ == '__main__':
    aws = get_aws_instance()
    destroy_infrastructure(aws)
