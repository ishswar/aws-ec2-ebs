#*****************************************
#Step 02: ec2run07_Part2a.py
#****************************************
#run this code after importing ec2run07.py
#into Python
import os
import random
import time
import boto3
import ec2run07_Part1

cwd=os.getcwd()
print('cwd=' + cwd)


inst = ec2run07_Part1.launch_instance()
instid=inst['InstanceId']

#volume must be in same availability zone as instance
azone=inst['Placement']['AvailabilityZone']
region='us-west-2'
ec2=boto3.client('ec2',region_name=region)
resp = ec2.create_volume(AvailabilityZone=azone, Size=2)
volume_id = resp['VolumeId']
print('created 2 gig volume in azone ' + azone + ' volumeId=' + volume_id)
volume_state = resp.get('State')
print('volume state=' + volume_state)

#wait for the volume to be ready if needed
bVolumeReady = False
if (volume_state != 'creating'):
    bVolumeReady = True

while not bVolumeReady:
    resp = ec2.describe_volumes(VolumeIds=[volume_id])
    volume_state = resp['Volumes'][0]['State']
    print('volume state = ' + volume_state)
    if (volume_state == 'available'):
        bVolumeReady = True
    else:
        print('Volume is not ready')
        time.sleep(2)

#attach volume to a device
resp = ec2.attach_volume(Device='/dev/sdf', InstanceId=instid,VolumeId=volume_id)
print('attached volume to EC2 instance')


# #create snapshot
# iz = random.randint(1, 9999999)
# snapshot_name = 'ucsc-aws-class-' + str(iz)
# resp = ec2.create_snapshot(Description=snapshot_name, VolumeId=volume_id)
# print(resp)
# snapshot_id = resp.get('SnapshotId')
# print('Created snapshot name=%s,id=%s' % (snapshot_name,snapshot_id))

#write the ec2 instance id into a file in the current directory
#call instid
filename = 'instidfile'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + instid + ' > ' + filename
os.system(bashcmd)

#write volume id out to a file
filename = 'volumeidfile'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + volume_id + ' > ' + filename
os.system(bashcmd)

# #write snapshot_id into a file
# filename = 'snapshotid'
# os.system('rm -f %s ' % filename)
# bashcmd = 'echo ' + snapshot_id + ' > ' + filename
# os.system(bashcmd)

exit(0)

#******************************************
#Next Step 03 is in ec2run07_Part2b.sh
#use ssh and the commands in ec2run07_Part2b.sh





