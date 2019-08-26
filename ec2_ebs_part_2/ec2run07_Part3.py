#********************************
#Step 04:
#********************************
#Run these Python commands after Step 03 in
#ec2Run07_Part2b.sh

import os
import boto3
import random
import time

#get instid from file instidfile
filename = './instidfile'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
instidP = fileobj.read()
instid = instidP.strip().strip('\n\r')
fileobj.close()

print('will create snapshot and terminate instance:' + instid)


filename = 'volumeidfile'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
volume_idP = fileobj.read()
volume_id = volume_idP.strip().strip('\n\r')

region='us-west-2'
ec2 = boto3.client('ec2', region_name=region)

#create snapshot
iz = random.randint(1, 9999999)
snapshot_name = 'ucsc-aws-class-' + str(iz)
resp = ec2.create_snapshot(Description=snapshot_name, VolumeId=volume_id)
print(resp)
snapshot_id = resp.get('SnapshotId')
print('Created snapshot name=%s,id=%s' % (snapshot_name, snapshot_id))

#write snapshot_id into a file
filename = 'snapshotid'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + snapshot_id + ' > ' + filename
os.system(bashcmd)

print('wrote snapshot-id into file')

#get instance, 
#technically speaking we do not need to get the instance id from ec2 since
#we already have it. The main point here is to learn about
#describe_instances
resp=ec2.describe_instances(InstanceIds=[instid])
instidfrom_ec2 = resp['Reservations'][0]['Instances'][0]['InstanceId']
print('instidfrom_ec2=' + instidfrom_ec2 + ' instanceidfrom_file=' + instid)

ec2.terminate_instances(InstanceIds=[instid])
print("terminated instance")
exit(0)

#***********************
#Next Step 05 is in ec2run07_Part4a.py


