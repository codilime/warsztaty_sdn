### Ważne komendy
0) Przygotowanie pod VM
```bash
sudo apt-get install virtualbox
sudo apt-get install vagrant
sudo git clone https://github.com/codilime/warsztaty_sdn
```

1) Tworzenie vmki
```bash
cd warsztaty_sdn/vm
vagrant up
```
==================================

Jeśli masz problem z vagrant, to zainstaluj tylko virtualbox
https://www.virtualbox.org/wiki/Downloads

1) Ściągnij VM z https://drive.google.com/drive/folders/1BbpQGiF4ytS52s7fT3CeeDeb9u63VYpz?usp=sharing

2) Zaimportuje VM w virtualbox

3) Ściągnij kod https://github.com/codilime/warsztaty_sdn

4) Udostępnij folder z kodem do vm pod ścieżkę /home/vagrant/warsztaty_sdn
* powinno wyglądać to tak jak w share.png

5) Przekieruj port 8090 guest na  8090 host oraz  8080 guest na 8081 host
* powinno wyglądać to tak jak w port.png

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
