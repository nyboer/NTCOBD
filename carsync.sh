#!/bin/bash
# need to wrap the mount and rsync into another script and call that script from here: ./actualscript.sh &

if [ $1 == wlan0 -a $2 == "up" ]; then
	echo "mounting DAV"
	sudo -u chip mount /mnt/dav
	#sleep 10
	if [ $? -eq 0 ]; then
		sudo -u chip rsync -apvz --delete --exclude '.*' /mnt/dav/ ~chip/Music/car
		sudo -u chip umount /mnt/dav
	else
		echo "Mount Failed"
	fi
else
	echo "network not up"
fi
