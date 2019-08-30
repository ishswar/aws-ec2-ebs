# aws-ec2-ebs
# Part 2 

  In this Boto3 example we will do this 
  
  1) Creating EC2 instance using Boto3 (in use-west-2 )
2) We will also create 3 volumes using Boto3 
3) We will attach volumes to EC2 instance that we created in step 1 
4) We will login via SSH (we will upload .sh file and do this) and mount these 3 volumes - write some test files 
5) Shutdown EC2 instance 
6) Create a snapshot of these 3 instances 
7) Deleting these 3 volumes as well 
8) Creating new EC2 instances 
9) Creating volumes from snapshots from step 6 
10) Again attaching the volumes and via SSH mounting them again back to this new EC2 instance 
11) We will see that files that we created in step 4 are still there
12) Once all done we will teardown the all the instance and volumes 

Below video shows steps 1 to 10

[![](http://img.youtube.com/vi/qSnlbtMrUKk/0.jpg)](http://www.youtube.com/watch?v=qSnlbtMrUKk "EC2 EBS Volume demo ")

#### Demo with just commands : 

[![asciicast](https://asciinema.org/a/XAyl80rTExVLYjlZ2f3BJjSH3.svg)](https://asciinema.org/a/XAyl80rTExVLYjlZ2f3BJjSH3)

Below video shows steps 12 about (teardown) 

![Cleanup](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_2/images/aws_ec2_ebs_cleanup.gif?raw=true)

## Python files

#### cleanDemoStuff.py :   

This file will be used to teardown, first it will delete EC2 instance then it will  
                    delete volumes and in last all the snapshots that we created during this demo . All the   
                    instance/volume/snapshot ID it gets it from temp files that we use to store this information  

#### createStart_EC2Inst.py :  

This is a helper class; it is used to create EC2 instances and wait for them to come up .  
It also has some helper functions    

#### runDEMO.py :  

This is a main file - it does all the steps described above (1 to 11)  
During program execution it uses temporory files to store EC2 instances , volume and snapshot id  

## Output

<details>
  <summary>Click to see full output</summary>

```bash
➜  ec2_ebs_part_2 git:(master) ✗ ./runDEMO.py
2019-08-29 14:48:11 =========================== Creating EC2 instance ============================
2019-08-29 14:48:12 EC2 instance has been created with ID : i-05e3a81e15d4dd5b3
  Now ... Waiting for instance to enter running state
2019-08-29 14:48:35 Instance is running now waiting for it to initialized
2019-08-29 14:48:35 Instance status : initializing
2019-08-29 14:49:21 Instance status : initializing
2019-08-29 14:50:06 Instance status : initializing
2019-08-29 14:50:51 Instance status : ok
2019-08-29 14:50:51 Checking if instance has Public IP - else we will wait for it be assigned
2019-08-29 14:50:51 Public IP assigned to this instance is: 34.213.241.250
2019-08-29 14:50:51 ============= Creating EBS volumes and attaching to EC2 instance =============
2019-08-29 14:50:51 [VOL-0]created 2 gig volume in azone us-west-2b volumeId=vol-0be26bfc21cf6f834
2019-08-29 14:50:51 [VOL-0]volume state=creating
2019-08-29 14:50:51 [VOL-0]volume state = creating
2019-08-29 14:50:51 [VOL-0]Volume is not ready
2019-08-29 14:50:53 [VOL-0]volume state = creating
2019-08-29 14:50:53 [VOL-0]Volume is not ready
2019-08-29 14:50:55 [VOL-0]volume state = creating
2019-08-29 14:50:55 [VOL-0]Volume is not ready
2019-08-29 14:50:58 [VOL-0]volume state = available
2019-08-29 14:50:58 [VOL-0]attached volume to EC2 instance
2019-08-29 14:50:58 [VOL-0]volume_id :vol-0be26bfc21cf6f834 has been saved to file: ./tempfiles/volumeidfile0
2019-08-29 14:50:58

2019-08-29 14:50:58 [VOL-1]created 2 gig volume in azone us-west-2b volumeId=vol-09211645e89e451a3
2019-08-29 14:50:58 [VOL-1]volume state=creating
2019-08-29 14:50:58 [VOL-1]volume state = creating
2019-08-29 14:50:58 [VOL-1]Volume is not ready
2019-08-29 14:51:00 [VOL-1]volume state = creating
2019-08-29 14:51:00 [VOL-1]Volume is not ready
2019-08-29 14:51:02 [VOL-1]volume state = available
2019-08-29 14:51:03 [VOL-1]attached volume to EC2 instance
2019-08-29 14:51:03 [VOL-1]volume_id :vol-09211645e89e451a3 has been saved to file: ./tempfiles/volumeidfile1
2019-08-29 14:51:03

2019-08-29 14:51:03 [VOL-2]created 2 gig volume in azone us-west-2b volumeId=vol-011d7d3acd61c88b7
2019-08-29 14:51:03 [VOL-2]volume state=creating
2019-08-29 14:51:03 [VOL-2]volume state = creating
2019-08-29 14:51:03 [VOL-2]Volume is not ready
2019-08-29 14:51:05 [VOL-2]volume state = creating
2019-08-29 14:51:05 [VOL-2]Volume is not ready
2019-08-29 14:51:07 [VOL-2]volume state = creating
2019-08-29 14:51:07 [VOL-2]Volume is not ready
2019-08-29 14:51:09 [VOL-2]volume state = available
2019-08-29 14:51:10 [VOL-2]attached volume to EC2 instance
2019-08-29 14:51:10 [VOL-2]volume_id :vol-011d7d3acd61c88b7 has been saved to file: ./tempfiles/volumeidfile2
2019-08-29 14:51:10

2019-08-29 14:51:10 ======================= Adding volumes to EC2 instance =======================
2019-08-29 14:51:10 Uploading Sell script that will create disk (form volumes) and map it to drive
2019-08-29 14:51:10 Command we are using is
scp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem /Users/pshah1/DevOps/AWS/ubuntuvm/aws-cli/w8/ec2_ebs_part_2/scripts/mapEBStoDriver.sh ec2-user@34.213.241.250:~
Warning: Permanently added '34.213.241.250' (ECDSA) to the list of known hosts.
mapEBStoDriver.sh                                                                                                                                                                                         100% 2478    89.3KB/s   00:00
2019-08-29 14:51:10 Now we will run above shell script (via SSH) to create mapping
 Command we are using is
ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@34.213.241.250 "./mapEBStoDriver.sh /dev/sdf /dev/sdg /dev/sdh"
List of partitions
major minor  #blocks  name

 202        0    8388608 xvda
 202        1    8386543 xvda1
 202       80    2097152 xvdf
 202       96    2097152 xvdg
output of lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0   8G  0 disk
└─xvda1 202:1    0   8G  0 part /
xvdf    202:80   0   2G  0 disk
xvdg    202:96   0   2G  0 disk
################ About to map 3 devices [/dev/sdf /dev/sdg /dev/sdh] to respetive drives #######################
[/dev/sdf] starting to work on device: /dev/sdf
[/dev/sdf] About to map device /dev/sdf as /mnt/data-store_0
[/dev/sdf] check data on device /dev/sdf
/dev/sdf: symbolic link to xvdf
[/dev/sdf] listing deviceName
/dev/sdf
[/dev/sdf] About to make a file system on device /dev/sdf , we will use ext4 file format
mke2fs 1.43.5 (04-Aug-2017)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: b24cc03d-581a-43b4-97b2-9308612b5ad2
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912

Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done

[/dev/sdf] Now lets mount /dev/sdf to drive /mnt/data-store_0
[/dev/sdf] CD in to new drive and create a sample file
[/dev/sdf] output of file that we just wrote
[/dev/sdf] ---------- START of file content ---------
        This is a sample text for file /dev/sdf on mapped driver /mnt/data-store_0
[/dev/sdf] ---------- END of file content --------




[/dev/sdg] starting to work on device: /dev/sdg
[/dev/sdg] About to map device /dev/sdg as /mnt/data-store_1
[/dev/sdg] check data on device /dev/sdg
/dev/sdg: symbolic link to xvdg
[/dev/sdg] listing deviceName
/dev/sdg
[/dev/sdg] About to make a file system on device /dev/sdg , we will use ext4 file format
mke2fs 1.43.5 (04-Aug-2017)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: 236fc820-8aa8-4e89-8d2c-1301425d240d
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912

Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done

[/dev/sdg] Now lets mount /dev/sdg to drive /mnt/data-store_1
[/dev/sdg] CD in to new drive and create a sample file
[/dev/sdg] output of file that we just wrote
[/dev/sdg] ---------- START of file content ---------
        This is a sample text for file /dev/sdg on mapped driver /mnt/data-store_1
[/dev/sdg] ---------- END of file content --------




[/dev/sdh] starting to work on device: /dev/sdh
[/dev/sdh] About to map device /dev/sdh as /mnt/data-store_2
[/dev/sdh] check data on device /dev/sdh
/dev/sdh: symbolic link to xvdh
[/dev/sdh] listing deviceName
/dev/sdh
[/dev/sdh] About to make a file system on device /dev/sdh , we will use ext4 file format
mke2fs 1.43.5 (04-Aug-2017)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: 97e243ef-d4bd-41b6-8496-cbf243040e66
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912

Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done

[/dev/sdh] Now lets mount /dev/sdh to drive /mnt/data-store_2
[/dev/sdh] CD in to new drive and create a sample file
[/dev/sdh] output of file that we just wrote
[/dev/sdh] ---------- START of file content ---------
        This is a sample text for file /dev/sdh on mapped driver /mnt/data-store_2
[/dev/sdh] ---------- END of file content --------




################ END OF device mapping #######################
All Mounting done lets see if it get listed in df command
Filesystem     Type     1K-blocks    Used Available Use% Mounted on
devtmpfs       devtmpfs    494100      72    494028   1% /dev
tmpfs          tmpfs       504748       0    504748   0% /dev/shm
/dev/xvda1     ext4       8189348 1129424   6959676  14% /
/dev/xvdf      ext4       1998672    6148   1871284   1% /mnt/data-store_0
/dev/xvdg      ext4       1998672    6148   1871284   1% /mnt/data-store_1
/dev/xvdh      ext4       1998672    6148   1871284   1% /mnt/data-store_2
2019-08-29 14:51:13 Now we will log-in again via SSH and check if files exists
 Command we are using is
ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@34.213.241.250 "ls -la /mnt/data-store_*"
/mnt/data-store_0:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:51 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_0.txt

/mnt/data-store_1:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:51 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_1.txt

/mnt/data-store_2:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:51 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_2.txt
2019-08-29 14:51:14 Sleeping 40 seconds so linux/OS can flush data to EBS before we take a snapshots
2019-08-29 14:51:54 ====================== will create snapshot of volumes =======================
2019-08-29 14:51:54 Creating snapshot for volume: vol-0be26bfc21cf6f834
2019-08-29 14:51:54 Created snapshot name=ucsc-aws-class-1753071,id=snap-0cff51451a59700c0
2019-08-29 14:51:54 wrote snapshot-id into file: ./tempfiles/snapshotid0
2019-08-29 14:51:54 Creating snapshot for volume: vol-09211645e89e451a3
2019-08-29 14:51:54 Created snapshot name=ucsc-aws-class-9099504,id=snap-02319784844cbe3bc
2019-08-29 14:51:54 wrote snapshot-id into file: ./tempfiles/snapshotid1
2019-08-29 14:51:55 Creating snapshot for volume: vol-011d7d3acd61c88b7
2019-08-29 14:51:55 Created snapshot name=ucsc-aws-class-6583968,id=snap-033ab34e8706200a7
2019-08-29 14:51:55 wrote snapshot-id into file: ./tempfiles/snapshotid2
2019-08-29 14:51:55 ==================== Terminating & Deleting EC2 instance =====================
2019-08-29 14:51:55 ============== Wait for Old EC2 instance is deleted and stopped ==============
2019-08-29 14:51:55  Wait for instance: i-05e3a81e15d4dd5b3to stop before we proceed with deleting volumes

2019-08-29 14:51:55 terminated instance
2019-08-29 14:51:55 Instance has not gone down yet .. will wait
2019-08-29 14:52:15 Instance has not gone down yet .. will wait
2019-08-29 14:52:35 ========================== will now delete volumes ===========================
2019-08-29 14:52:35 Deleting volume:vol-0be26bfc21cf6f834
2019-08-29 14:52:35 Deleted volume: vol-0be26bfc21cf6f834
2019-08-29 14:52:35 Deleting volume:vol-09211645e89e451a3
2019-08-29 14:52:36 Deleted volume: vol-09211645e89e451a3
2019-08-29 14:52:36 Deleting volume:vol-011d7d3acd61c88b7
2019-08-29 14:52:36 Deleted volume: vol-011d7d3acd61c88b7
2019-08-29 14:52:36 ============= Create new EC2 instance for attaching volumes back =============
2019-08-29 14:52:37 EC2 instance has been created with ID : i-0380337ce7ba10e59
  Now ... Waiting for instance to enter running state
2019-08-29 14:53:00 Instance is running now waiting for it to initialized
2019-08-29 14:53:00 Instance status : initializing
2019-08-29 14:53:45 Instance status : initializing
2019-08-29 14:54:30 Instance status : initializing
2019-08-29 14:55:15 Instance status : initializing
2019-08-29 14:56:00 Instance status : ok
2019-08-29 14:56:00 Checking if instance has Public IP - else we will wait for it be assigned
2019-08-29 14:56:00 Public IP assigned to this instance is: 54.184.233.79
2019-08-29 14:56:00 wrote new instance id out to file ./tempfiles/instidfile
2019-08-29 14:56:00 ===== Create a new volumes from snapshot and then attach to EC2 instance =====
2019-08-29 14:56:00 using snapshot-id:snap-0cff51451a59700c0
2019-08-29 14:56:01 created volume vol-08e540fce043d60e7 in availability-zone us-west-2b from snapshot=snap-0cff51451a59700c0
2019-08-29 14:56:01 volume state=creating
2019-08-29 14:56:01 volume state = creating
2019-08-29 14:56:01 Volume is not ready
2019-08-29 14:56:21 volume state = available
2019-08-29 14:56:21 [VOL-0]volume_id :vol-08e540fce043d60e7 has been saved to file: ./tempfiles/volumeidfile0
2019-08-29 14:56:21

2019-08-29 14:56:21 attached volume to EC2 instance
2019-08-29 14:56:21 using snapshot-id:snap-02319784844cbe3bc
2019-08-29 14:56:21 created volume vol-0f998d306540d37d9 in availability-zone us-west-2b from snapshot=snap-02319784844cbe3bc
2019-08-29 14:56:21 volume state=creating
2019-08-29 14:56:21 volume state = creating
2019-08-29 14:56:21 Volume is not ready
2019-08-29 14:56:42 volume state = available
2019-08-29 14:56:42 [VOL-1]volume_id :vol-0f998d306540d37d9 has been saved to file: ./tempfiles/volumeidfile1
2019-08-29 14:56:42

2019-08-29 14:56:42 attached volume to EC2 instance
2019-08-29 14:56:42 using snapshot-id:snap-033ab34e8706200a7
2019-08-29 14:56:42 created volume vol-091f13d08ad2e39e2 in availability-zone us-west-2b from snapshot=snap-033ab34e8706200a7
2019-08-29 14:56:42 volume state=creating
2019-08-29 14:56:42 volume state = creating
2019-08-29 14:56:42 Volume is not ready
2019-08-29 14:57:02 volume state = available
2019-08-29 14:57:02 [VOL-2]volume_id :vol-091f13d08ad2e39e2 has been saved to file: ./tempfiles/volumeidfile2
2019-08-29 14:57:02

2019-08-29 14:57:03 attached volume to EC2 instance
2019-08-29 14:57:03 ================ Re-mapping volumes back to new EC2 instance =================
2019-08-29 14:57:03 Uploading Sell script that will create disk (form volumes) and map it as drive
2019-08-29 14:57:03 Command we are using is
scp -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem /Users/pshah1/DevOps/AWS/ubuntuvm/aws-cli/w8/ec2_ebs_part_2/scripts/mapEBSasDriveDirect.sh ec2-user@54.184.233.79:~
Warning: Permanently added '54.184.233.79' (ECDSA) to the list of known hosts.
mapEBSasDriveDirect.sh                                                                                                                                                                                    100% 1890    66.0KB/s   00:00
2019-08-29 14:57:03 Now we will run above shell script (via SSH) to create mapping
 Command we are using is
ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@54.184.233.79 "./mapEBSasDriveDirect.sh /dev/sdf /dev/sdg /dev/sdh"
List of partitions
major minor  #blocks  name

 202        0    8388608 xvda
 202        1    8386543 xvda1
 202       80    2097152 xvdf
 202       96    2097152 xvdg
output of lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0   8G  0 disk
└─xvda1 202:1    0   8G  0 part /
xvdf    202:80   0   2G  0 disk
xvdg    202:96   0   2G  0 disk
Total # volumes listed in lsblk output are 5
Total # volumes listed in lsblk output are 6
we found our voluems that we were expeting;lets mount them
output of df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        483M   72K  483M   1% /dev
tmpfs           493M     0  493M   0% /dev/shm
/dev/xvda1      7.9G  1.1G  6.7G  14% /
Above output of 'lsblk' should show there are 3 devices but they are not mapped to any drives (eveident from 'df -h' ouput)
################ About to re-map/re-mount 3 devices [/dev/sdf /dev/sdg /dev/sdh] to respetive drives #######################
[/dev/sdf] starting to work on device: /dev/sdf
[/dev/sdf] About to map device /dev/sdf as /mnt/dz_0
[/dev/sdf] Done mounting volume /dev/sdf


[/dev/sdg] starting to work on device: /dev/sdg
[/dev/sdg] About to map device /dev/sdg as /mnt/dz_1
[/dev/sdg] Done mounting volume /dev/sdg


[/dev/sdh] starting to work on device: /dev/sdh
[/dev/sdh] About to map device /dev/sdh as /mnt/dz_2
[/dev/sdh] Done mounting volume /dev/sdh


################ END OF device re-mapping #######################
All Mounting done lets see if it get listed in df command
Filesystem     Type     1K-blocks    Used Available Use% Mounted on
devtmpfs       devtmpfs    494100      72    494028   1% /dev
tmpfs          tmpfs       504748       0    504748   0% /dev/shm
/dev/xvda1     ext4       8189348 1129416   6959684  14% /
/dev/xvdf      ext4       1998672    6148   1871284   1% /mnt/dz_0
/dev/xvdg      ext4       1998672    6148   1871284   1% /mnt/dz_1
/dev/xvdh      ext4       1998672    6148   1871284   1% /mnt/dz_2
list files in all new mapped drives (we should see our old files still present there)
ls -la /mnt/dz_0 /mnt/dz_1 /mnt/dz_2
2019-08-29 14:57:14 Now we will log-in again via SSH and check if files exists
 Command we are using is
ssh -i ../../../../../AWS/ubuntuvm/pshah2019v2.pem ec2-user@54.184.233.79 "ls -la /mnt/dz_*"
/mnt/dz_0:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:57 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_0.txt

/mnt/dz_1:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:57 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_1.txt

/mnt/dz_2:
total 28
drwxrwxrwx 3 root     root      4096 Aug 29 21:51 .
drwxr-xr-x 5 root     root      4096 Aug 29 21:57 ..
drwx------ 2 root     root     16384 Aug 29 21:51 lost+found
-rw-rw-r-- 1 ec2-user ec2-user    83 Aug 29 21:51 testFile_2.txt
2019-08-29 14:57:14 =========================== ---- END of Demo ----- ===========================
2019-08-29 14:57:14 =======
*** Note ***
Run cleanDemoStuff.py to tear everything down =======
```
</details>

### Screen capture 

![AWS Console](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_2/images/AWS_Console_showing_final_instance.jpg?raw=true)

# Part 1 

## Introduction 

  (This is a simpler version of above 
    - we do lot of thing manually and only create/mount one EBS volume)
  
  In this boto3 example we will do this 
  
-   Create EC2 instance and on additional 2GB Volume
-   (Manual step) Log-in to instance via SSH and mount volume and create some
    files 
-   Take a snapshot of Volume and delete EC2 instance 
-   Create new EC2 instance , create a new volume from above snapshot and 
    attach to this EC2 instance 
-   (Manual step) log-in to instance and mount volume and see if files created
    previously are still there
-   Finally delete EC2 instance , Volume and snapshot  
  
## Screen captures 
  
### Creating Instance/Volume 

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_Create_EC2_Voluem_1.jpg?raw=true)

### Second volume attached to EC2 instance 

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_EC2_instance_volumes_attached_2.jpg?raw=true)

### Mounting volume as drive using SSH

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_SSH_Mounting_volume_as_drive_3.jpg?raw=true)

### Creating snapshot from volume  

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_Snapshot_of_volume_4.jpg?raw=true)

### Snapshot in AWS Console  

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_Snapshot_of_volume_AWS_Console_4.jpg?raw=true)

### Creating new volume using Snapshot  

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_EC2_Attaching_volume_from_Snapshot_5.jpg?raw=true)

### AWS Console showing volume as been created from snapshot   

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_New_Volume_from_snapshot_6.jpg?raw=true)

### Mounting new volume as drive via SSH ( getting old files back )  

![alt text](https://github.com/ishswar/aws-ec2-ebs/blob/master/ec2_ebs_part_1/part1_SSH_Mounting_Volume_and_retriveing_filesback_7.jpg?raw=true)
