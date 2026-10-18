eim-cli#!/bin/bash

sudo apt update
sudo apt -y upgrade

sudo debconf-set-selections <<EOF
iptables-persistent iptables-persistent/autosave_v4 boolean true
iptables-persistent iptables-persistent/autosave_v6 boolean true
EOF

sudo apt install -y dnsmasq iptables-persistent

cat ~/multipass-orchestrator-configurations/lab-env/keys.txt >>  ~/.ssh/authorized_keys
sudo cp ~/multipass-orchestrator-configurations/ota-server-rpi/dnsmasq.conf /etc
sudo cp ~/multipass-orchestrator-configurations/ota-server-rpi/iptables.rules /etc/iptables/rules.v4

sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo systemctl mask systemd-resolved

sudo rm /etc/resolv.conf
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf

sudo sed -i "s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/" /etc/sysctl.conf

echo "192.168.100.254 ota.marsattacks.com" | sudo tee -a /etc/hosts
echo "192.168.100.254 router router.marsattacks.com" | sudo tee -a /etc/hosts
# set static IP addresses, change to your requirements
echo "dhcp-host=xx:xx:xx:xx,pc,192.168.100.100" | sudo tee -a /etc/dnsmasq.conf

sudo apt install -y nginx

# Install the Espressif signing key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://dl.espressif.com/dl/eim/eim.gpg -o /etc/apt/keyrings/eim.gpg
sudo chmod 0644 /etc/apt/keyrings/eim.gpg

# Add the Espressif APT repository (deb822 with signed-by)
sudo curl -fsSL https://dl.espressif.com/dl/eim/eim.sources -o /etc/apt/sources.list.d/espressif.sources

# Update package lists
sudo apt update

# Install CLI only
sudo apt install -y eim-cli

eim install

sudo reboot
