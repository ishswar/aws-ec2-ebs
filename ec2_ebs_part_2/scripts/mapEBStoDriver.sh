#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'No arguments were provided - we need on input with space seperated deviceNames'
    exit 1
fi

if [ -z "$1" ] ; then
    echo 'No arguments were provided - we need on input with space seperated deviceNames'
    exit 1
fi


listofDrives=("$@")

total=${#listofDrives[*]}
#

    echo "List of partitions"
    cat /proc/partitions
    echo "output of lsblk"
    lsblk

echo "################ About to map $total devices ["$@"] to respetive drives #######################"

for (( i=0; i<=$(( $total -1 )); i++ ))
do 
    #echo  "${listofDrives[$i]}"

    deviceName=${listofDrives[$i]}
    echo "[$deviceName] starting to work on device: $deviceName"
    targetDrive="/mnt/data-store_$i"

    echo "[$deviceName] About to map device $deviceName as $targetDrive"

    #check for data on the device
    #sdf is actually a symlink to xvdf
    echo "[$deviceName] check data on device $deviceName"
    sudo file -s $deviceName

    #/dev/xvdf: data - if you see output that says "data" it means there is
    #no data on the device
    #sudo file -s /dev/xvdf
    echo "[$deviceName] listing deviceName"
    ls $deviceName

    #create a filesystem on sdf, again sdf is a symlink for  xvdf
    echo "[$deviceName] About to make a file system on device $deviceName , we will use ext4 file format"
    sudo mke2fs -t ext4 -F -j $deviceName

    #now that the device has a filesystem on it, mount it
    echo "[$deviceName] Now lets mount $deviceName to drive $targetDrive"
    sudo mkdir $targetDrive
    sudo mount $deviceName $targetDrive
    echo "[$deviceName] CD in to new drive and create a sample file "
    cd $targetDrive
    sudo chmod 777 .

    #type something in, whatever you type in gets into file cats.txt
    #hit return followed by control-d to get out of the ca
    cat > "testFile_$i.txt" <<EOF
        This is a sample text for file $deviceName on mapped driver $targetDrive
EOF
    echo "[$deviceName] output of file that we just wrote "
    echo "[$deviceName] ---------- START of file content ---------"
    cat "testFile_$i.txt"
    echo "[$deviceName] ---------- END of file content --------"
    echo
    echo
    echo
    echo



    #now see if there is data in the volume
    #you will see several things including ext4
    #sudo file -s /dev/xvdf



done
    echo "################ END OF device mapping #######################"

    echo "All Mounting done lets see if it get listed in df command "
    df -T