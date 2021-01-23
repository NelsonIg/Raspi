# Raspi
Setup Raspi and Mosquitto

## Image
Download  [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/)
## Wifi and SSH
+ Load empty file "ssh" on SD Card
+ create 'wpa_supplicant.conf' like below:

```
country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
       ssid="Wifi Name"
       psk="Wifi Password"
       key_mgmt=WPA-PSK
}
```
More info [here](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
+ Connect via ssh
```
ssh hostname@ip
```
hostname might be raspberrypi or pi, also mdns might be supported from beginning:
```
ssh pi@raspberrypi.local or pi@pi.local
```
## Mosquitto
```
https://mosquitto.org/man/mosquitto-8.html
https://mosquitto.org/man/mosquitto_sub-1.html
https://mosquitto.org/man/mosquitto_pub-1.html

sudo apt update
sudo apt install mosquito
sudo apt install mosquitto-clients

mosquitto -d (deamon)
sudo service mosquitto status

sudo service mosquitto stop
alternativ:
	netstat -at -- PID finden
	kill <pid>
```
