### Ważne komendy
0) Przygotowanie pod VM
```bash
sudo apt-get install virtualbox
sudo apt-get install vagrant
```

1) Tworzenie vmki
```bash
vagrant up
```

Kredki ubuntu/ubuntu

2) Wchodzenie do vm
```bash
vagrant ssh
```

Opcjonalne
3) budowanie images (vm)
```bash
cd /home/vagrant/warsztaty_sdn
ansible-playbook -i inv.yml playbooks/build.yml
```

4) Uruchamianie kontroller i rutera (vm)
```bash
cd /home/vagrant/warsztaty_sdn
ansible-playbook -i inv.yml playbooks/run.yml
```

5) Restartowanie kontroller i rutera (vm)
```bash
cd /home/vagrant/warsztaty_sdn
docker-compose restart
```



### Jeśli nie masz linuxa tu są linki do vagrant i virtualboxa


[vagrant](https://www.vagrantup.com/downloads.html)

[virtualbox](https://www.virtualbox.org/wiki/Downloads)
