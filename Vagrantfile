# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  
  config.vm.provision   "file", source: "./Dockerfile", 
                        destination: "/vagrant/app/Dockerfile"
  config.vm.provision   "file", source: "./splunk-launch.conf", 
                        destination: "/vagrant/app/splunk-launch.conf"

  config.vm.provision "docker" do |d|
    d.build_image "/vagrant/app", args: '--build-arg="RELEASE_URL=7.3.6/linux/splunk-7.3.6-47d8552a4d84-Linux-x86_64.tgz" --target=base -t splunk-enterprise'
  end


  config.vm.define "manager" do |man|
    man.vm.network :private_network, ip: "192.168.33.10"
    man.vm.provision  "file", source: "./server-master.conf", 
                      destination: "/vagrant/app/server-master.conf"
    man.vm.provider :virtualbox do |vb|
      vb.name = "splunk-manager"
    end
    man.vm.provision "docker" do |d|
      d.build_image "/vagrant/app", args: '--target=manager -t splunk-manager'
      d.run "splunk-manager", image: "splunk-manager", args: "-p 8000:8000 -p 8089:8089"
    end
  end

  (1..2).each do |i|
    config.vm.define "sh#{i}" do |shcl|
      shcl.vm.network :private_network, ip: "192.168.33.1#{i}"
      shcl.vm.provision "file", source: "./server-sh.conf", 
                        destination: "/vagrant/app/server-sh.conf"
      shcl.vm.provider :virtualbox do |vb|
        vb.name = "splunk-sh-#{i}"
      end
      shcl.vm.provision "docker" do |d|
        d.build_image "/vagrant/app", args: '--target=sh -t splunk-sh'
        d.run "splunk-sh", image: "splunk-sh", args: "-p 8000:8000 -p 8089:8089"
      end
    end
  end

  (1..2).each do |i|
    config.vm.define "idx#{i}" do |idx|
      idx.vm.network :private_network, ip: "192.168.33.2#{i}"
      idx.vm.provision  "file", source: "./server-idx.conf", 
                        destination: "/vagrant/app/server-idx.conf"
      idx.vm.provider :virtualbox do |vb|
        vb.name = "splunk-idx-#{i}"
      end
      idx.vm.provision "docker" do |d|
        d.build_image "/vagrant/app", args: '--target=idx -t splunk-idx'
        d.run "splunk-idx", image: "splunk-idx", args: "-p 8000:8000 -p 8080:8080 -p 8089:8089"
      end
    end
  end
end
