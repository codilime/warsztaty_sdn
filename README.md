## Przygtowanie 

1) Ściągnij vagrant z [vagrant](https://www.vagrantup.com/downloads.html)

2) Zainstaluj vagrant 

3) Sprawdź czy to wersja  2.0.x

4) Ściągnij virtualbox z [virtualbox](https://www.virtualbox.org/wiki/Downloads)
* dla Windowsa nie ma jeszcze 5.2 dlatego trzeba sciągnąć 5.1 [virtualbox-old](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

5) Zainstaluj virtualbox

6) Sprawdź czy wersja to 5.x.x

7) Zainstaluj extension pack [virtualbox-ext](https://download.virtualbox.org/virtualbox/5.2.8/Oracle_VM_VirtualBox_Extension_Pack-5.2.8.vbox-extpack)

8) Zainstaluj vagrant [disksize](https://github.com/sprotheroe/vagrant-disksize)
```bash
vagrant plugin install vagrant-disksize
```


## Gotowa vm
ściągnąc box z https://drive.google.com/open?id=16P8mRc6J9kblMDr6mPsCQ35eL0BVmyNP

vagrantfile powinien wyglądać tak:

```yaml
Vagrant.configure("2") do |config|
  config.ssh.username = 'vagrant'
  config.ssh.password = 'vagrant'
  config.vm.box = "polibuda-sdn-ready.box"
  config.vm.define "polibuda-sdn-ready"
  config.disksize.size = "16GB"
  config.vm.synced_folder "save/", "/home/vagrant/Desktop/save"
  config.vm.provider "virtualbox" do |vb|
    vb.name = "polibuda-sdn-ready"
    vb.gui = true
    vb.memory = 2048
    vb.cpus = 2
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end
end

```

## Uruchomienie VM

```bash
cd vm
vagrant up

```

# Od tej pory pracujemy tylko w vm

## Jak uruchomić synchornizacje folderu save

```bash
sudo -i
cd /home/vagrant/Desktop/save
git clone https://github.com/codilime/warsztaty_sdn.git
cd warsztaty_sdn
ansible-playbook -i inv.yml ssh.yml
```

## Rozpoczęcie pracy

```bash
sudo -i
cd /home/vagrant/Desktop/save
git clone https://github.com/codilime/warsztaty_sdn.git
cd warsztaty_sdn
ansible-playbook -i inv.yml clean.yml
ansible-playbook -i inv.yml run.yml
```