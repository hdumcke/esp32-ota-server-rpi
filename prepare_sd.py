#!/usr/bin/env python3
import argparse
import sys
import os

##############################################################
#
# Ask questions to prepare cloud-init file for mini pupper
#
# if ~/.TeamCdR2024_sd.txt exists no questions will be asked
#
##############################################################

target_environment = {}


def write_cache(cache_file):
    with open(cache_file, 'w') as fh:
        for key in target_environment.keys():
            fh.write("%s: %s\n" % (key, target_environment[key]))


def ask_user(prompt, var_name):
    input_text = input("%s: " % prompt)
    target_environment[var_name] = input_text


def ask_questions():
    if 'wifi_ssid' not in target_environment.keys():
        ask_user("Your WiFi SSID", 'wifi_ssid')
    if 'wifi_password' not in target_environment.keys():
        ask_user("Your WiFi password", 'wifi_password')
    if 'user_name' not in target_environment.keys():
        ask_user("Your user name", 'user_name')
    if 'user_password' not in target_environment.keys():
        ask_user("Your user password", 'user_password')
    if 'user_ssh_key' not in target_environment.keys():
        ask_user("Your user ssh key", 'user_ssh_key')
    if 'keyboard_layout' not in target_environment.keys():
        ask_user("Your keyboard layout (fr or us)", 'keyboard_layout')
    if 'sd_path' not in target_environment.keys():
        ask_user("Full path to SD card", 'sd_path')


# Detect OS
target_environment['this_os'] = sys.platform

parser = argparse.ArgumentParser(description='Prepare SD card for Mini Pupper')
parser.add_argument('-c', '--cache',
                    action='store_true',
                    help='Cache my responses')
args = parser.parse_args()

conf_file = os.path.join(os.path.expanduser("~"), '.TeamCdR2024_sd.txt')
if os.path.exists(conf_file):
    with open(conf_file, 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if ':' in line:
                arr = line.strip().split(':')
                key = arr[0]
                if len(arr) == 2:
                    value = arr[1].strip()
                else:
                    value = ''.join(s for s in arr[1:]).strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                if len(value) > 0:
                    target_environment[key] = value
ask_questions()

if args.cache:
    write_cache(conf_file)

network_conf_file = os.path.join(target_environment['sd_path'], 'network-config')
if not os.path.exists(network_conf_file):
    sys.exit("Invalid path to SD card or SD card not mounted\n")

network_conf = """network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      dhcp6: no
      addresses: [192.168.100.254/24]
      optional: true
  wifis:
    wlan0:
      dhcp4: true
      regulatory-domain: "FR"
      access-points:
        "%s":
          password: "%s"
          type: text
      optional: true
"""

with open(network_conf_file, 'w') as fh:
    fh.write(network_conf % (target_environment['wifi_ssid'], target_environment['wifi_password']))

user_data_file = os.path.join(target_environment['sd_path'], 'user-data')

user_data = """#cloud-config
manage_resolv_conf: false
hostname: marsattacks
manage_etc_hosts: false
packages:
- avahi-daemon
- git

runcmd:
- [ git, clone, "https://github.com/hdumcke/multipass-orchestrator-configurations.git" ]
- [ "/home/%s/multipass-orchestrator-configurations/ota-server-rpi/build.sh 2>> /home/%s/.setup_err.log >> /home/%s/.setup_out.log" ]
apt:
  preserve_sources_list: true
  conf: |
    Acquire {
      Check-Date "false";
    };
timezone: Europe/Paris
keyboard:
  model: pc105
  layout: "%s"
users:
- name: %s
  groups: users,adm,dialout,audio,netdev,video,plugdev,cdrom,games,input,gpio,spi,i2c,render,sudo
  shell: /bin/bash
  lock_passwd: false
  passwd: "%s"
  type: text
  ssh_authorized_keys:
    - %s
  sudo: ALL=(ALL) NOPASSWD:ALL
enable_ssh: true
ssh_pwauth: false
"""
with open(user_data_file, 'w') as fh:
    fh.write(user_data % (target_environment['user_name'], target_environment['user_name'], target_environment['user_name'], target_environment['keyboard_layout'], target_environment['user_name'], target_environment['user_password'], target_environment['user_ssh_key']))

print("Flashed cloud-config successfully")
