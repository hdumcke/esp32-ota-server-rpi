Build the ESP32 OTA example
===========================

Run

```
eim select
```

And select the environment you want to use. Issue the source command as indicated

Then
```
cd ~/.espressif/v6.1/esp-idf/examples/system/ota/native_ota_example/
idf.py menuconfig
```

In the Example Connection Configuration menu:

- provide the Wi-Fi SSID and password of the AP
- disable ipv6

In the Example Configuration menu:

- Set the URL of the firmware to download in the Firmware Upgrade URL to : https://ota.marsattacks.com/native_ota.bin

Then build the project:
```
idf.py all
```

Copy server certs:
```
openssl x509 -in ~/pki-example-1/ca/root-ca.crt -out ~/.espressif/v6.1/esp-idf/examples/system/ota/native_ota_example/server_certs/ca_cert.pem
```

Copy firmware to web server:
```
sudo cp build/native_ota.bin /usr/share/nginx/html/
```

Flash the project:
```
idf.py flash
```

Build updated version of firmware and copy to web server:
```
echo 2 > version.txt
idf.py all
sudo cp build/native_ota.bin /usr/share/nginx/html/
```

Test:
```
screen /dev/ttyUSB0 115200
```

(in new termina connection)
```
cd ~/.espressif/v6.1/esp-idf/examples//get-started/hello_world
sed -i "s/Restarting/Restarting(new)/" main/hello_world_main.c
idf.py all
sudo cp build/native_ota.bin /usr/share/nginx/html/
```
