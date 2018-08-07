sudo chmod +x startup.sh 
sudo chmod +x init.sh 
sudo chmod +x /usr/bin/myprompt 
sudo chmod +x detect_attY.sh

find /home/icub -maxdepth 1 -mindepth 1 -type f | sudo parallel --no-notice chown -R icub
find /home/icub/.local -maxdepth 1 -mindepth 1 -type d | sudo parallel --no-notice chown -R icub
find $SRC_FOLDER -maxdepth 1 -mindepth 1 -type d | sudo parallel --no-notice chown -R icub 
find /home/icub/user_files/Deep_Speech -maxdepth 1 -mindepth 1 -type d | sudo parallel --no-notice chown -R icub
#sudo chown -R icub /home/icub/user_files/Deep_Speech
#sudo chown -R icub /home/icub/user_files/Sheffield-XPrize