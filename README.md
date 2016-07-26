OBD on pocket chip
sudo apt-get install -y screen openssh-server x11vnc bluez-tools rfkill
sudo apt-get install -y samba cifs-utils smbclient

sudo apt-get install -y python-setuptools python-dev build-essential 
sudo easy_install pip 
sudo pip install --upgrade virtualenv 
pip install obd
pip install subprocess
https://gist.github.com/egorf/66d88056a9d703928f93

for cairo graphics?
sudo apt-get install libffi-dev0
sudo pip install cffi
sudo pip install cairocffi


Connect to ODB II Bluetooth device:
	bluetoothctl
at bluetoothctl prompt, use:
	agent on
	power on
	scan on
	pair <MAC>
	if pin, then 1234
	trust <MAC>
	ctl-D
in bash:
	sudo rfcomm connect hci0 <MAC>
now
	screen /dev/rfcomm0
and follow this guide for basic serial commands
	http://gersic.com/connecting-your-raspberry-pi-to-a-bluetooth-obd-ii-adapter/
We can now proceed to installing pyserial and pyodb to actually do something with this data
We can use https://github.com/brendan-w/python-OBD to provide an interface to the ODB commands.
This has some ui widgets https://github.com/brendan-w/piHud

http://python-obd.readthedocs.io/en/latest/Connections/

interesting, but not useful for PocketCHIP since we can't programatically mount and sync with SMB on CHIP, 
but follow this guide to create a SMB share NAS with CHIP:
https://pimylifeup.com/raspberry-pi-nas/

For what it’s worth, this mount doesn't work! We need to modify the kernel:
	sudo mount -t cifs //10.0.0.100/NASCHIP /mnt/nas  -o “username=naschip,password=chip”

Sync with home directory

apt-get install davfs2 rsync

Basic WebDAV mounting is like so:
chip@pocketcar:~$ sudo mount -t davfs http://www.yowstar.com/out /mnt/dav
Please enter the username to authenticate with server
http://www.nbor.us/car or hit enter for none.
  Username: xl92

rsync -avz --delete --exclude '.*' /mnt/dav/ ~/Music/car

https://<WebDav URI> <mount point> davfs user,noauto,file_mode=600,dir_mode=700 0 1


Basic idea:
Setup a WebDAV service - various options to do this. Using dreamhost. Could setup up webdav with dropbox or owncloud.
Setup PocketCHIP to mount webdav with a simple command and no credentials using this guide:
http://techiech.blogspot.com/2013/04/mounting-webdav-directory-in-linux.html
	except put secrets in /etc/davfs2/secrets
	don’t uncomment the line
	add user with sudo usermod -a -G davfs2 chip
	and reboot
	then you can mount with mount /mnt/dav

Make a Network Manager script that will get called when a wireless network is up:
/etc/NetworkManager/dispatcher.d/carsync.sh
on up, it tries to mount the webdav, then sync files to a home directory 
	Can you make WebDAV add/force permissions?
Need to have NetworkManager call a script that calls a script in the background in hopes of this escaping NM's 90 second timeout. Must test this! 

Of course, this sync only happens when a network is connected. What if you want to force a sync?
maybe keep mount up and have a watcher observe for changes or run a chron job 

