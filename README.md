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
