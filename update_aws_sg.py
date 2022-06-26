import requests
import boto3
from botocore.exceptions import ClientError

GROUP_ID = 'GROUP-ID'
RULE_DESCRIPTION = 'Rule Description'
NEW_IP = requests.get('http://checkip.amazonaws.com').text[:-1] + '/32'
OLD_IP = ''

ec2 = boto3.client('ec2')

try:
    response = ec2.describe_security_groups(GroupIds=[GROUP_ID])
except ClientError as e:
    print(e)

sg = response['SecurityGroups']
for el in range(len(sg)):
    if sg[el]['GroupId'] == GROUP_ID:
        ip_pems = sg[el]['IpPermissions']
        for i in range(len(ip_pems)):
            if ip_pems[i]['IpRanges'][0]['Description'] == RULE_DESCRIPTION:
                OLD_IP = ip_pems[i]['IpRanges'][0]['CidrIp']
                print('Old office Ip %s' % OLD_IP)

if (OLD_IP != NEW_IP) & (OLD_IP != ''):
    try:
        d = ec2.revoke_security_group_ingress(
            GroupId = GROUP_ID,
            IpPermissions=[
                {
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': OLD_IP,
                            'Description': RULE_DESCRIPTION
                        }
                    ]
                }
            ]
        )
        print('Ingress successfully removed %s' % d)
    except ClientError as e:
        print(e)
    
    try:
        d = ec2.authorize_security_group_ingress(
            GroupId = GROUP_ID,
            IpPermissions=[
                {
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': NEW_IP,
                            'Description': RULE_DESCRIPTION
                        }
                    ]
                }
            ]
        )
        print('Ingress successfully set %s' % d)
    except ClientError as e:
        print(e)
