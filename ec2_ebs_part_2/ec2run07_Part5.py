#********************************
#Step 07: ec2run_Part5.py
# cleanup aws resources
#********************************

import os
import time
import boto3


region='us-west-2'
ec2 = boto3.client('ec2', region_name=region)


################################################
#delete ec2 instance
filename = './instidfile'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
instidP = fileobj.read()
instid = instidP.strip().strip('\n\r')
fileobj.close()

#terminate ec2 instance
print('will delete instance-id:' + instid)
ec2.terminate_instances(InstanceIds=[instid])

sleeptime = 10
bIsRunning = True
while bIsRunning == True:
    rz=ec2.describe_instance_status(InstanceIds=[instid])
    #call can return before all data is available
    if not bool(rz):
        time.sleep(sleeptime)
        continue
    if len(rz["InstanceStatuses"]) == 0:
        break;

    inststate=rz["InstanceStatuses"][0]["InstanceState"]
    #print(json.dumps(inststate,indent=2,separators=(',',':')))
    state=inststate["Name"]
    if state == 'terminated' or state == 'shutting-down' or  state == 'stopping':
        bIsRunning = False
    
    print('waiting for ec2 instance to stop')
    time.sleep(sleeptime)

print("EC2 instance is termniated")


################################################
#delete volume
filename = 'volumeidfile'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
volume_idP = fileobj.read()
volume_id = volume_idP.strip().strip('\n\r')
print('will delete volume-id:' + volume_id)
ec2.delete_volume(VolumeId=volume_id)


################################################
#delete snapshot
filename = './snapshotid'
if os.path.exists(filename) == False:
    print(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
snapidP = fileobj.read()
snapid = snapidP.strip().strip('\n\r')
fileobj.close()
print("will delete snapshot-id:" + snapid)
ec2.delete_snapshot(SnapshotId=snapid)


print('***** all done *****')
exit(0)

