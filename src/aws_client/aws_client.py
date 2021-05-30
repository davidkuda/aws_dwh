import json

import boto3
import pandas as pd

from utils import parse_configs, get_secrets


class AWS:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str,
                 region: str, config_params: dict):
        self.aws_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region)
        self.s3 = self.aws_session.resource('s3')
        self.ec2 = self.aws_session.resource('ec2')
        self.iam = self.aws_session.client('iam')
        self.redshift = self.aws_session.client('redshift')
        self.configs = config_params

    def create_iam_role(self):
        role_policy = {
            'Statement': [
                {'Action': 'sts:AssumeRole',
                 'Effect': 'Allow',
                 'Principal': {'Service': 'redshift.amazonaws.com'}
                 }
            ]}

        dwh_role = self.iam.create_role(
            Path='/',
            RoleName=self.configs.get('DWH_IAM_ROLE_NAME'),
            Description='Allows Redshift clusters to call AWS services on your behalf.',
            AssumeRolePolicyDocument=json.dumps(role_policy))

        self.iam.attach_role_policy(
            RoleName=self.configs.get('DWH_IAM_ROLE_NAME'),
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess')
        # ['ResponseMetadata']['HTTPStatusCode']

        role_arn = self.iam.get_role(
            RoleName=self.configs.get('DWH_IAM_ROLE_NAME')
        )['Role']['Arn']

        return role_arn

    def create_redshift_cluster(self, role_arn):
        response = self.redshift.create_cluster(
            # HW / hardware
            ClusterType=self.configs.get('DWH_CLUSTER_TYPE'),
            NodeType=self.configs.get('DWH_NODE_TYPE'),
            NumberOfNodes=int(self.configs.get('DWH_NUM_NODES')),

            # Identifiers & Credentials
            DBName=self.configs.get('DWH_DB'),
            ClusterIdentifier=self.configs.get('DWH_CLUSTER_IDENTIFIER'),
            MasterUsername=self.configs.get('DWH_DB_USER'),
            MasterUserPassword=self.configs.get('DWH_DB_PASSWORD'),

            # Roles (for s3 access)
            IamRoles=[role_arn]
        )

        print(response)

    @staticmethod
    def get_redshift_props_as_pd_df(redshift_props):
        pd.set_option('display.max_colwidth', None)
        keys_to_show = ["ClusterIdentifier", "NodeType", "ClusterStatus",
                        "MasterUsername", "DBName", "Endpoint",
                        "NumberOfNodes", 'VpcId']
        x = [(k, v) for k, v in redshift_props.items() if k in keys_to_show]
        return pd.DataFrame(data=x, columns=["Key", "Value"])

    def open_tcp_port(self, cluster_props):
        vpc = self.ec2.Vpc(id=cluster_props['VpcId'])
        default_security_group = list(vpc.security_groups.all())[0]
        default_security_group.authorize_ingress(
            GroupName=default_security_group.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(self.configs.get('DWH_PORT')),
            ToPort=int(self.configs.get('DWH_PORT')))

    def delete_cluster(self):
        self.redshift.delete_cluster(
            ClusterIdentifier=self.configs['DWH_CLUSTER_IDENTIFIER'],
            SkipFinalClusterSnapshot=True)

    def delete_iam_role(self):
        self.iam.detach_role_policy(
            RoleName=self.configs['DWH_IAM_ROLE_NAME'],
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
        self.iam.delete_role(RoleName=self.configs['DWH_IAM_ROLE_NAME'])


def get_redshift_cluster_props():
    redshift_cluster_props = aws.redshift.describe_clusters(
        ClusterIdentifier=configs.get('DWH_CLUSTER_IDENTIFIER')
    )['Clusters']
    return redshift_cluster_props


def create_infrastructure(aws: AWS):

    aws.create_iam_role()

    role_arn = aws.iam.get_role(
        RoleName=configs.get('DWH_IAM_ROLE_NAME')
    )['Role']['Arn']

    aws.create_redshift_cluster(role_arn)


def do_sth(redshift_cluster_props):
    DWH_ENDPOINT = redshift_cluster_props['Endpoint']['Address']
    DWH_ROLE_ARN = redshift_cluster_props['IamRoles'][0]['IamRoleArn']
    print(DWH_ENDPOINT)
    print(DWH_ROLE_ARN)


def open_tcp_port(aws: AWS, redshift_cluster_props) -> None:
    aws.open_tcp_port(redshift_cluster_props)


def check_redshift_status(aws: AWS, redshift_cluster_props):
    df = aws.get_redshift_props_as_pd_df(redshift_cluster_props)
    print(df)


def destroy_infrastructure(aws: AWS):
    aws.delete_cluster()
    aws.delete_iam_role()


if __name__ == '__main__':
    configs = parse_configs('../../config/dwh.cfg')
    secrets = get_secrets()

    aws = AWS(aws_access_key_id=secrets.get('KEY'),
              aws_secret_access_key=secrets.get('SECRET'),
              region=configs.get('REGION'),
              config_params=configs)

    # Create the Redshift Cluster and wait until available
    # create_infrastructure(aws)

    # Check for availability
    redshift_cluster_props = get_redshift_cluster_props()[0]
    check_redshift_status(aws, redshift_cluster_props)
    do_sth(redshift_cluster_props)

    # After cluster is available: Open tcp port.
    # open_tcp_port(aws, redshift_cluster_props)

    # Finally, destroy infrastructure.
    # destroy_infrastructure(aws)