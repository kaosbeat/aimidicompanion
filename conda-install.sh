FILE=/home/vagrant/aimidicompanion/Anaconda3-2019.03-Linux-x86_64.sh
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
fi
bash ~/aimidicompanion/Anaconda3-2019.03-Linux-x86_64.sh