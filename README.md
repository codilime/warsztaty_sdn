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

4) Udostępnij folder z kodem do vm, jak nazwę podaj warsztaty_sdn
* powinno wyglądać to tak jak w share.png


Kredki ubuntu/ubuntu

1) Wchodzenie do vm
```bash
vagrant ssh
```

Opcjonalne
2) budowanie images (vm)
```bash
cd /home/vagrant/warsztaty_sdn
./build.sh
```

3) Uruchamianie kontroller i rutera (vm)
```bash
cd /home/vagrant/warsztaty_sdn
./run.sh
```

4) Restartowanie kontroller i rutera (vm)
```bash
cd /home/vagrant/warsztaty_sdn
docker-compose restart
```

5) Uruchamianie komend na kontenerze
```bash
docker exec <nazwa kontenera> <komenda>
```
Przykłady:
Sprawdzanie adresu ip
```bash
docker exec ala ifconfig
```

Pingowanie
```bash
docker exec ala ping 192.168.0.3 -c 1
```


### Jeśli nie masz linuxa tu są linki do vagrant i virtualboxa


[vagrant](https://www.vagrantup.com/downloads.html)

[virtualbox](https://www.virtualbox.org/wiki/Downloads)
