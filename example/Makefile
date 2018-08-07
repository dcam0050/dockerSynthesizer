.PHONY: build first_run run clean docker configure build_image buildBashrc uploadImage upload

tagName := dcamilleri13/icub-client
containerName := icub-client
#scan parts directory
INPUTS := $(wildcard ${DOCKERPARTS}/*.part)
HOST=$(shell hostname)

build: clean docker build_image buildBashrc build_image1

run:
	docker start $(containerName)
	docker attach $(containerName)

clean:
	@rm -f bashrc_iCub
	@rm -f Dockerfile
	-@docker rm -f $(containerName) >/dev/null || true
	touch bashrc_iCub

docker:
	${DOCKERPARTS}/compileDockerfile.py $(PWD)

configure:
	sudo apt-get install -y libopenni-dev squid-deb-proxy


first_run:
	docker run -dit --env="DISPLAY="${DISPLAY} --env="QT_X11_NO_MITSHM=1" 					\
					  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" 									\
					  --volume=/dev/snd:/dev/snd													\
					  --volume="/home/$(USER)/.local/share/yarp:/home/icub/.local/share/yarp:rw" 	\
					  --volume="/dev/bus/usb:/dev/bus/usb"											\
					  --name=${containerName} 														\
					  --hostname=$(HOST)															\
					  --network=host																\
					  --privileged 																	\
					  $(tagName)
	docker stop $(containerName)
	#set up display
	@xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $(containerName)`
	docker start $(containerName)
	docker attach $(containerName)

build_image build_image1:
	docker build -t $(tagName) .
	-@docker stop $(containerName) >/dev/null || true
	-@docker rm $(containerName) >/dev/null || true

	docker run -dit --env="DISPLAY="${DISPLAY} --env="QT_X11_NO_MITSHM=1" 					\
					  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" 									\
					  --volume=/dev/snd:/dev/snd													\
					  --volume="/home/$(USER)/.local/share/yarp:/home/icub/.local/share/yarp:rw" 	\
					  --volume="/dev/bus/usb:/dev/bus/usb"											\
					  --name=${containerName} 														\
					  --hostname=$(HOST)															\
					  --network=host																\
					  --privileged 																	\
					  $(tagName)
	docker stop $(containerName)
	#set up display
	@xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $(containerName)`

buildBashrc:
	#set up environment bashrc_iCub
	$(eval envVars = $(shell docker inspect --format='{{.Config.Env}}' $(containerName))) \
	$(eval envVars = $(envVars) | cut -c 31- | rev | cut -c 2- | rev)\
	$(eval envVars = $(shell echo  $(envVars)))
	@echo "export "$(envVars) > bashrc_iCub
	@echo "source ~/.sourceScripts" >> bashrc_iCub
	@echo "environment written to bashrc_iCub"

all: build run

upload: build uploadImage

uploadImage: 
	docker push $(tagName)

