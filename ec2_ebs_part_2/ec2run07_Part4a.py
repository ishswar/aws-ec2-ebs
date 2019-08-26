#********************************
#Step 05: ec2run_Part4a.py
#********************************

import os
import time
import boto3
import ec2run07_Part1


region='us-west-2'
ec2=boto3.client('ec2',region_name=region)

filename = './snapshotid'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
snapidP = fileobj.read()
snapid = snapidP.strip().strip('\n\r')
fileobj.close()
print("using snapshot-id:" + snapid)


#create another instance, we will attach another EBS volume
#using the snapshot we saved earlier
inst = ec2run07_Part1.launch_instance()
instid = inst['InstanceId']

filename = 'instidfile'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + instid + ' > ' + filename
os.system(bashcmd)
print('wrote new instance id out to file ' + filename)

azone=inst['Placement']['AvailabilityZone']

#create volume from snapshot
resp=ec2.create_volume(AvailabilityZone=azone,SnapshotId=snapid)
volume_id = resp['VolumeId']
print('created volume " + volume_id +  " in availability-zone ' + azone + ' from snapshot=' + snapid)

volume_state = resp.get('State')
print('volume state=' + volume_state)

#wait for the volume to be ready if needed
bVolumeReady = False
if (volume_state != 'creating'):
    bVolumeReady = True

#wait for voulme to become available
while not bVolumeReady:
    resp = ec2.describe_volumes(VolumeIds=[volume_id])
    volume_state = resp['Volumes'][0]['State']
    print('volume state = ' + volume_state)
    if (volume_state == 'available'):
        bVolumeReady = True
    else:
        print('Volume is not ready')
        time.sleep(20)

#attach volume to EC2 instance
#attach volume to a device
resp = ec2.attach_volume(Device='/dev/sdf', InstanceId=instid,VolumeId=volume_id)
print('attached volume to EC2 instance')

exit(0)


#***************************************************
# Next ec2run07_Part4b.sh
#


#cleanup commands for latter
#ec2.terminate_instances(InstanceIds=[instid])
#ec2.delete_snapshot(SnapshotId=snapid)
#ec2.delete_volume(VolumeId=volume_id)












