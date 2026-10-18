ESP32 OTA server on Raspberry Pi 4
==================================

This project installs a test environment for OTA on a Raspberry Pi 4. It requires a WiFi access point (lab AP)  that is configured with a SSID and password. The access point serves as the WiFi network for the ESP32.

The Raspberry Pi connects to a WiFi network that provides internet access. For development purposes a PC can connect to the lab AP.

The Raspberry Pi runs a DHCP and a DNS server as well as a web server to serve the OTA images. It also provides an environment to build a certificate authority tool chain to generate a certificate for OTA. The Raspberry Pi is set up with the ESP32 development environment.

Tidbit
------

MarsAttacks is the name of our team for [Coupe de France de Robotique](https://www.coupederobotique.fr)

Installation
------------

Prepare SD card with Ubuntu 24.04 Server using the Raspberry Pi Imager. Mount SD on PC and run

```
./prepare_sd.py
```

or on Windows

```
./prepare_sd.bat
```

Once the Sd card is prepared boot Raspberry Pi 4 off this card and wait until it reboots. Then follow with README_ca, README_nginx and README_esp32.
