# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  config.vm.network "private_network", type: "dhcp"

  (50000...50010).each { |port|
    config.vm.network :forwarded_port, guest: port, host: port
  }

  config.vm.provider "virtualbox" do |vb|
    vb.name = "mini-docker"
    vb.gui = false
    vb.cpus = 1
    vb.memory = "1024"
  end

  config.vm.provision "shell", path: "provisioner.sh"
end
