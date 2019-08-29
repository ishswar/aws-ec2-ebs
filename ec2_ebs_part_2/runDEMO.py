#!/usr/bin/env python3
# *****************************************
# Step 02: runDEMO.py
# ****************************************
# run this code after importing ec2run07.py
# into Python
import os
import subprocess
import random
import time
import boto3
import createStart_EC2Inst

cwd = os.getcwd()
#print('cwd=' + cwd)

volumeNames = ["/dev/sdf", "/dev/sdg", "/dev/sdh"]
allDrives = ""
for i in range(len(volumeNames)):
    allDrives = allDrives + " " + volumeNames[i]
allDrives = str.strip(allDrives)

"""
### Launch EC2 instance 
"""
createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Creating EC2 instance"))
inst = createStart_EC2Inst.launch_instance()
instid = inst['InstanceId']

"""
### Create volumes and attach to above EC2 instance 
"""
createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Creating EBS volumes and attaching to EC2 instance"))
for i in range(len(volumeNames)):
    # volume must be in same availability zone as instance
    azone = inst['Placement']['AvailabilityZone']
    region = 'us-west-2'
    ec2 = boto3.client('ec2', region_name=region)
    resp = ec2.create_volume(AvailabilityZone=azone, Size=2)
    volume_id = resp['VolumeId']
    createStart_EC2Inst.printlog(
        '[VOL-' + str(i) + ']' + 'created 2 gig volume in azone ' + azone + ' volumeId=' + volume_id)
    volume_state = resp.get('State')
    createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'volume state=' + volume_state)

    # wait for the volume to be ready if needed
    bVolumeReady = False
    if (volume_state != 'creating'):
        bVolumeReady = True

    while not bVolumeReady:
        resp = ec2.describe_volumes(VolumeIds=[volume_id])
        volume_state = resp['Volumes'][0]['State']
        createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'volume state = ' + volume_state)
        if (volume_state == 'available'):
            bVolumeReady = True
        else:
            createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'Volume is not ready')
            time.sleep(2)

    # attach volume to a device
    resp = ec2.attach_volume(Device=volumeNames[i], InstanceId=instid, VolumeId=volume_id)
    createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'attached volume to EC2 instance')

    # write volume id out to a file
    filename = './tempfiles/volumeidfile' + str(i)
    os.system('rm -f %s ' % filename)
    bashcmd = 'echo ' + volume_id + ' > ' + filename
    os.system(bashcmd)
    createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'volume_id :' + volume_id + ' has been saved to file: ' + filename)
    createStart_EC2Inst.printlog('\n\r')

# write the ec2 instance id into a file in the current directory
# call instid
filename = './tempfiles/instidfile'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + instid + ' > ' + filename
os.system(bashcmd)

"""
###  Mount all 3 volumes to Linux OS - via SSH
"""

publicip = inst.get('PublicIpAddress')

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Adding volumes to EC2 instance"))
createStart_EC2Inst.printlog("Uploading Sell script that will create disk (form volumes) and map it to drive")

filename = './scripts/mapEBStoDriver.sh'
if os.path.exists(filename) == False:
    createStart_EC2Inst.printlog(filename + " does not exist - we need this to proceed")
    exit(1)

createStart_EC2Inst.banner("SSH login and run Shell script to map/mount volumes")
createStart_EC2Inst.printlog(
    "Command we are using is \n\rscp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem " + cwd + "/scripts/mapEBStoDriver.sh "
                                                                                              "ec2-user@" + publicip + ":~")
subprocess.call(
    'scp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ' + cwd + '/scripts/mapEBStoDriver.sh ec2-user@' + publicip + ':~',
    shell=True)
command = 'ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@' + publicip + ' "./mapEBStoDriver.sh ' + allDrives + '"'
createStart_EC2Inst.printlog(
    "Now we will run above shell script (via SSH) to create mapping \n\r Command we are using is \n\r" + command)

subprocess.call(command, shell=True)

command = 'ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@' + publicip + ' "ls -la /mnt/data-store_*"'
createStart_EC2Inst.printlog(
    "Now we will log-in again via SSH and check if files exists \n\r Command we are using is \n\r" + command)

subprocess.call(command, shell=True)

"""
### Take a snapshot of Volumes , delete volumes and delete instances
"""

createStart_EC2Inst.printlog("Sleeping 40 seconds so linux/OS can flush data to EBS before we take a snapshots")
time.sleep(40)
createStart_EC2Inst.printlog(createStart_EC2Inst.banner('will create snapshot of volumes'))
for i in range(len(volumeNames)):

    filename = './tempfiles/volumeidfile' + str(i)
    if os.path.exists(filename) == False:
        createStart_EC2Inst.printlog(filename + " does not exist")
        exit(1)

    fileobj = open(filename, 'r')
    volume_idP = fileobj.read()
    volume_id = volume_idP.strip().strip('\n\r')

    region = 'us-west-2'
    ec2 = boto3.client('ec2', region_name=region)

    # create snapshot
    iz = random.randint(1, 9999999)
    snapshot_name = 'ucsc-aws-class-' + str(iz)
    resp = ec2.create_snapshot(Description=snapshot_name, VolumeId=volume_id)
    # ec2run07_Part1.printlog(resp)
    snapshot_id = resp.get('SnapshotId')
    createStart_EC2Inst.printlog("Creating snapshot for volume: " + volume_id)
    createStart_EC2Inst.printlog('Created snapshot name=%s,id=%s' % (snapshot_name, snapshot_id))

    # write snapshot_id into a file
    filename = './tempfiles/snapshotid' + str(i)
    os.system('rm -f %s ' % filename)
    bashcmd = 'echo ' + snapshot_id + ' > ' + filename
    os.system(bashcmd)

    createStart_EC2Inst.printlog('wrote snapshot-id into file: ' + filename)


"""
### Delete the EC2 instance 1
"""

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Terminating & Deleting EC2 instance"))
createStart_EC2Inst.printlog(createStart_EC2Inst.banner('Wait for Old EC2 instance is deleted and stopped'))
createStart_EC2Inst.printlog(createStart_EC2Inst.banner('Wait for instance: ' + instid + 'to stop before we proceed with '
                                                                               'deleting volumes' + '\n\r'))

ec2.terminate_instances(InstanceIds=[instid])
createStart_EC2Inst.printlog("terminated instance")

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

"""
### Delete volumes that we created for Instance 1 ; we don't need them - we have snapshots of them
"""

createStart_EC2Inst.printlog(createStart_EC2Inst.banner('will now delete volumes'))
for i in range(len(volumeNames)):

    try:
        filename = './tempfiles/volumeidfile' + str(i)
        if os.path.exists(filename) == False:
            createStart_EC2Inst.printlog(filename + " does not exist")
            exit(1)

        fileobj = open(filename, 'r')
        volume_idP = fileobj.read()
        volume_id = volume_idP.strip().strip('\n\r')

        createStart_EC2Inst.printlog('Deleting volume:' + volume_id)
        ec2.delete_volume(VolumeId=volume_id)
        createStart_EC2Inst.printlog('Deleted volume: ' + volume_id)
    except Exception as e:
        createStart_EC2Inst.printlog("ERROR: "+ str(e))
        pass

"""
### Create new EC2 instance
"""

createStart_EC2Inst.printlog(createStart_EC2Inst.banner('Create new EC2 instance for attaching volumes back'))
# create another instance, we will attach another EBS volume
# using the snapshot we saved earlier
inst = createStart_EC2Inst.launch_instance()
instid = inst['InstanceId']
publicip = inst.get('PublicIpAddress')

filename = './tempfiles/instidfile'
os.system('rm -f %s ' % filename)
bashcmd = 'echo ' + instid + ' > ' + filename
os.system(bashcmd)
createStart_EC2Inst.printlog('wrote new instance id out to file ' + filename)

"""
Take a snapshot of Volumes , delete volumes and delete instances
"""

createStart_EC2Inst.printlog(createStart_EC2Inst.banner('Create a new volumes from snapshot and then attach to EC2 '
                                                        'instance'))
for i in range(len(volumeNames)):

    filename = './tempfiles/./snapshotid' + str(i)
    if os.path.exists(filename) == False:
        createStart_EC2Inst.printlog(filename + " does not exist")
        exit(1)

    fileobj = open(filename, 'r')
    snapidP = fileobj.read()
    snapid = snapidP.strip().strip('\n\r')
    fileobj.close()
    createStart_EC2Inst.printlog("using snapshot-id:" + snapid)

    azone = inst['Placement']['AvailabilityZone']

    # create volume from snapshot
    resp = ec2.create_volume(AvailabilityZone=azone, SnapshotId=snapid)
    volume_id = resp['VolumeId']
    createStart_EC2Inst.printlog(
        'created volume ' + volume_id + ' in availability-zone ' + azone + ' from snapshot=' + snapid)

    volume_state = resp.get('State')
    createStart_EC2Inst.printlog('volume state=' + volume_state)

    # wait for the volume to be ready if needed
    bVolumeReady = False
    if (volume_state != 'creating'):
        bVolumeReady = True

    # wait for voulme to become available
    while not bVolumeReady:
        resp = ec2.describe_volumes(VolumeIds=[volume_id])
        volume_state = resp['Volumes'][0]['State']
        createStart_EC2Inst.printlog('volume state = ' + volume_state)
        if (volume_state == 'available'):
            bVolumeReady = True
        else:
            createStart_EC2Inst.printlog('Volume is not ready')
            time.sleep(20)

    # write volume id out to a file
    filename = './tempfiles/volumeidfile' + str(i)
    os.system('rm -f %s ' % filename)
    bashcmd = 'echo ' + volume_id + ' > ' + filename
    os.system(bashcmd)
    createStart_EC2Inst.printlog('[VOL-' + str(i) + ']' + 'volume_id :' + volume_id + ' has been saved to file: ' + filename)
    createStart_EC2Inst.printlog('\n\r')

    # attach volume to EC2 instance
    # attach volume to a device

    resp = ec2.attach_volume(Device=volumeNames[i], InstanceId=instid, VolumeId=volume_id)
    createStart_EC2Inst.printlog('attached volume to EC2 instance')

"""
### Log-in to EC2 instance and re-map/re-mount volumes in OS so we can use it
"""

#time.sleep(40)
createStart_EC2Inst.printlog(createStart_EC2Inst.banner("Re-mapping volumes back to new EC2 instance"))
createStart_EC2Inst.printlog("Uploading Sell script that will create disk (form volumes) and map it as drive")

filename = './scripts/mapEBSasDriveDirect.sh'
if os.path.exists(filename) == False:
    createStart_EC2Inst.printlog(filename + " does not exist - we need this mapEBSasDriveDirect.sh proceed")
    exit(1)

createStart_EC2Inst.banner("SSH login and run Shell script to re-map/mount volumes")
createStart_EC2Inst.printlog(
    "Command we are using is \n\rscp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem " + cwd + "/scripts/mapEBSasDriveDirect.sh "
                                                                                              "ec2-user@" + publicip + ":~")
subprocess.call(
    'scp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ' + cwd + '/scripts/mapEBSasDriveDirect.sh ec2-user@' + publicip + ':~',
    shell=True)
command = 'ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@' + publicip + ' "./mapEBSasDriveDirect.sh ' + allDrives + '"'
createStart_EC2Inst.printlog(
    "Now we will run above shell script (via SSH) to create mapping \n\r Command we are using is \n\r" + command)

subprocess.call(command, shell=True)

command = 'ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@' + publicip + ' "ls -la /mnt/dz_*"'
createStart_EC2Inst.printlog(
    "Now we will log-in again via SSH and check if files exists \n\r Command we are using is \n\r" + command)

subprocess.call(command, shell=True)


createStart_EC2Inst.printlog(createStart_EC2Inst.banner("---- END of Demo -----"))

createStart_EC2Inst.printlog(createStart_EC2Inst.banner("\n\r*** Note *** \n\rRun cleanDemoStuff.py to tear everything down"))
