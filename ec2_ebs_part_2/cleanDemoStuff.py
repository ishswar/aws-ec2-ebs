#!/usr/bin/env python3

# ********************************
# Step 07: ec2run_Part5.py
# cleanup aws resources
# ********************************

import os
import time
import boto3
import createStart_EC2Inst

region = 'us-west-2'
ec2 = boto3.client('ec2', region_name=region)

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Deleting EC2 instance"))
################################################
# delete ec2 instance
filename = './tempfiles/instidfile'
if os.path.exists(filename) == False:
    createStart_EC2Inst.printlog(filename + " does not exist")
    exit(1)

fileobj = open(filename, 'r')
instidP = fileobj.read()
instid = instidP.strip().strip('\n\r')
fileobj.close()

# terminate ec2 instance
createStart_EC2Inst.printlog('will delete instance-id:' + instid)
ec2.terminate_instances(InstanceIds=[instid])

createStart_EC2Inst.printlog("Instance terminated")

bGotIp = False
while bGotIp == False:
    terminatereply = ec2.terminate_instances(InstanceIds=[instid])
    currentInstanceState = terminatereply["TerminatingInstances"][0]["CurrentState"]["Name"]
    if not currentInstanceState == 'terminated':
        createStart_EC2Inst.printlog('Instance has not gone down yet .. will wait')
        time.sleep(20)
        continue
    else:
        bGotIp = True

createStart_EC2Inst.printlog("EC2 instance is stoped and terminated")

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Deleting EBS volumes"))
################################################
# delete volume
for i in range(3):
    filename = './tempfiles/volumeidfile' + str(i)
    if os.path.exists(filename) == False:
        createStart_EC2Inst.printlog(filename + " does not exist")
        exit(1)

    fileobj = open(filename, 'r')
    volume_idP = fileobj.read()
    volume_id = volume_idP.strip().strip('\n\r')
    createStart_EC2Inst.printlog('will delete volume-id:' + volume_id)
    ec2.delete_volume(VolumeId=volume_id)

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Deleting Snapshots"))
################################################
# delete snapshot
for i in range(3):
    filename = './tempfiles/./snapshotid' + str(i)
    if os.path.exists(filename) == False:
        createStart_EC2Inst.printlog(filename + " does not exist")
        exit(1)

    fileobj = open(filename, 'r')
    snapidP = fileobj.read()
    snapid = snapidP.strip().strip('\n\r')
    fileobj.close()
    createStart_EC2Inst.printlog("will delete snapshot-id:" + snapid)
    ec2.delete_snapshot(SnapshotId=snapid)

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Deleting Temp files"))
for i in range(3):
    filename = './tempfiles/./snapshotid' + str(i)
    if os.path.exists(filename):
        createStart_EC2Inst.printlog("Deleting [snapshot-id] temp file: " + filename)
        os.remove(filename)

    filename = './tempfiles/volumeidfile' + str(i)
    if os.path.exists(filename):
        createStart_EC2Inst.printlog("Deleting [volume-id] temp file: " + filename)
        os.remove(filename)

filename = './tempfiles/instidfile'
if os.path.exists(filename):
    createStart_EC2Inst.printlog("Deleting [instance-id] temp file: " + filename)
    os.remove(filename)

createStart_EC2Inst.printlog('***** all done *****')
exit(0)
