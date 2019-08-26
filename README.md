# aws-ec2-ebs

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
