Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 8989, host: 8988
  config.vm.synced_folder "~/aimidicompanion", "/home/vagrant/aimidicompanion"
  #config.vm.provision "shell", inline: "apt-get update"
  #config.vm.provision "shell", inline: "apt-get install -y gcc g++"
  #config.vm.provision "shell", inline:  "apt-get install -y alsa-utils libsndfile1"
  #config.vm.provision "file", source: "~/aimidicompanion", destination: "~/aimidicompanion"
  #config.vm.provision "shell", inline: "bash ~/aimidicompanion/conda-install.sh", privileged: false
  #config.vm.provision "shell", inline: "bash ~/aimidicompanion/magenta-install.sh", privileged: false

end
