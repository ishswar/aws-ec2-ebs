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

    while true; do
      totalVolumes=$(lsblk | wc -l);
      echo "Total # volumes listed in lsblk output are $totalVolumes";
      if [[ $totalVolumes -eq 6 ]] ;
       then echo "we found our voluems that we were expeting;lets mount them";
       break;
      else sleep 10;
      fi;
    done

    echo "output of df -h"
    df -h
    echo "Above output of 'lsblk' should show there are 3 devices but they are not mapped to any drives (eveident from 'df -h' ouput)"


echo "################ About to re-map/re-mount $total devices ["$@"] to respetive drives #######################"

for (( i=0; i<=$(( $total -1 )); i++ ))
do 
    #echo  "${listofDrives[$i]}"

    deviceName=${listofDrives[$i]}
    echo "[$deviceName] starting to work on device: $deviceName"
    targetDrive="/mnt/dz_$i"

    allDrives="$allDrives $targetDrive"

    echo "[$deviceName] About to map device $deviceName as $targetDrive"


    sudo mkdir $targetDrive
    sudo mount $deviceName $targetDrive -t ext4
    echo "[$deviceName] Done mounting volume $deviceName"
    echo
    echo



    #now see if there is data in the volume
    #you will see several things including ext4
    #sudo file -s /dev/xvdf



done
    echo "################ END OF device re-mapping #######################"

    echo "All Mounting done lets see if it get listed in df command "
    df -T
    echo "list files in all new mapped drives (we should see our old files still present there)"
    echo ls -la $allDrives