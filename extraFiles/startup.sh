#!/usr/bin/env bash
DIR="/home/icub/.local/share/yarp/contexts/himrep/IOL2OPCDatabase"
sudo service ssh start
sudo service postgresql start

if sudo service ssh status | grep not
then 
  	echo "SSH not running. Cannot start demo";
else
	echo "SSH running"
   	sudo rm -r $DIR/*

	if [ "$(ls -A $DIR)" ]; then
	     echo "Error deleting IOL2OPCDatabase objects"
	else
		echo "Deleted IOL2OPCDatabase objects"
		if aplay ~/Xylo.wav | grep cannot
		then
			echo "No audio output. Check PULSE_SERVER settings";
		else
			echo "Audio working"
		    icub-cluster.py &
			xterm -e yarpmanager &
			xterm -e "myprompt pc104 yarprobotinterface" &
			xterm -e 'myprompt daniel-beast "yarp rpc /actionsRenderingEngine/cmd:io"' &
			xterm &
		fi
	fi
fi
