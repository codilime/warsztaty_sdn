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
## Budowanie od zera
```bash
cd build_vm
vagrant up

```
## Gotowa vm
ściągnąc box z https://drive.google.com/open?id=1cpKalme36MYi4QiJENTZw2ul_Z44XdJe

```bash
cp  polibuda-sdn-ready.box ready_vm/
cd ready_vm
vagrant up

```
