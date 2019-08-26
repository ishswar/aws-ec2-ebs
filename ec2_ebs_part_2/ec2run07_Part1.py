# *************************
# Step 01: Load this into Python first
# *************************

import os
import time
import sys
import boto3
import botocore
import botocore.exceptions
from botocore.exceptions import ClientError
import json


# import boto.vpc

# NOTE: you will have  to change the default parameter values
#      to your values, or pass them in when making the function call
def launch_instance(amiid='ami-0f2176987ee50226e',
                    instance_type='t2.micro',
                    keypair_name='pshah2019v2',
                    security_group_name='awsclass01a',
                    cidr='0.0.0.0/0',
                    tag='lpsiinst01',
                    user_data=None,
                    region='us-west-2'):
    # Create a connection to EC2 service and get vpc connection
    ec2 = boto3.client('ec2', region_name=region)

    # get the 1st vpc and 1st subnet
    resp = ec2.describe_vpcs()
    vpcidtouse = resp['Vpcs'][0]['VpcId']
    subnetlist = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpcidtouse]}])
    subnetid = subnetlist['Subnets'][0]['SubnetId']

    # Check to see if specified security group already exists.
    # If we get an InvalidGroup.NotFound error back from EC2,
    # it means that it doesn't exist and we need to create it.
    secgrpname = security_group_name
    bcreatedsecgrp = False
    try:
        secgrpfilter = [
            {
                'Name': 'group-name', 'Values': [secgrpname]
            }
        ]
        secgroups = ec2.describe_security_groups(
            Filters=secgrpfilter
        )
        if secgroups['SecurityGroups']:
            secgrptouse = secgroups["SecurityGroups"][0]
            secgrpid = secgrptouse['GroupId']
        else:
            secgrptouse = ec2.create_security_group(
                GroupName=secgrpname, Description='aws class open ssh,http,https',
                VpcId=vpcidtouse)
            secgrpid = secgrptouse['GroupId']
            bcreatedsecgrp = True
    except ClientError as e:
        print("%s " % e.response['Error']['Code'])
        raise

    if (bcreatedsecgrp == True):
        # Add a rule to the security group to authorize ssh traffic
        # on the specified port.
        # open ports 22, 80, 443,
        portlist = [22, 80, 443]
        for port in portlist:
            try:
                ec2.authorize_security_group_ingress(
                    CidrIp='0.0.0.0/0',
                    FromPort=port,
                    GroupId=secgrpid,
                    IpProtocol='tcp',
                    ToPort=port)
            except:
                print("error opening port:" + str(port))
                exit()

    try:
        secgrpidlist = [secgrpid]
        numinstances = 1
        resp = ec2.run_instances(
            ImageId=amiid,
            InstanceType=instance_type,
            KeyName=keypair_name,
            SecurityGroupIds=secgrpidlist,
            SubnetId=subnetid,
            MaxCount=numinstances,
            MinCount=numinstances)
    except:
        print("exception:", sys.exc_info()[0])
        raise

    # The instance has been launched but it's not yet up and
    # running.  Let's wait for it's state to change to 'running'.

    print('waiting for instance')
    inst = resp["Instances"][0]
    instid = inst["InstanceId"]
    print('Waiting for instance to enter running state')

    bIsRunning = False
    while bIsRunning == False:
        rz = ec2.describe_instance_status(InstanceIds=[instid])
        # call can return before all data is available
        if not bool(rz):
            # sys.stdout.write('.')
            continue
        if len(rz["InstanceStatuses"]) == 0:
            # sys.stdout.write('.')
            continue

        inststate = rz["InstanceStatuses"][0]["InstanceState"]
        print(json.dumps(inststate, indent=2, separators=(',', ':')))
        state = inststate["Name"]
        if state == 'running':
            bIsRunning = True
        # else:
        # sys.stdout.write('.')
        #

    print('EC2 instance is running')
    return inst

# inst = launch_instance()
