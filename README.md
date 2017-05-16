# dockerSynthesizer
Collection of scripts to assemble dockerfiles and docker images in a modular way. 

Each .part file contains install instructions and environment variables for a particular library. 

To use, first add $DOCKERPARTS environment variable pointing to the base directory to your bashrc.

Then copy contents of example directory to the directory where you want to compile your dockerfile and customise metafile to contain all your required libraries. Makefile will then run a script to synthesize the docker file and subsequently build and run it.

Omit .part when listing libraries inside of metafile.
compileDockerfile.py checks that all libraries in metafile have their corresponding .part counterparts and then assembles the dockerfile. It also scans the .part files and copies files required for any `ADD` or `COPY` command from the extra files directory to your build directory.

Warning: Dockerfile compilation currently does not take into consideration pre-requisites for the compilation of .part files. This must be taken care of by the user.
