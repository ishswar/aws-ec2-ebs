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

Below video shows steps 12 about (teardown) 

# Part 1 

## Introduction 

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
