#!/usr/bin/env sh

set -ex

cat <<EOF
------------------------------
install required packages
------------------------------
EOF

apt update
apt upgrade -y
apt install -y python3-distutils python3-pip bridge-utils cgroup-tools
pip3 install pipenv

cat <<EOF
------------------------------
enable ip forward
------------------------------
EOF
echo 1 > /proc/sys/net/ipv4/ip_forward
echo '/proc/sys/net/ipv4/ip_forward'
cat /proc/sys/net/ipv4/ip_forward


cat <<EOF
------------------------------
initialize iptables [NAT]
------------------------------
EOF

iptables --table nat --flush

# mini-dockerのサブネットからの送信がinternetに出られるように設定
iptables --table nat --append POSTROUTING --source 192.168.0.0/24 --jump MASQUERADE

iptables --table nat --list


cat <<EOF
------------------------------
install python syscall library
------------------------------
EOF

cd /vagrant/libs
python3 ./setup.py install

cat <<EOF
------------------------------
install python library to system
------------------------------
EOF

cd /vagrant
pipenv install --system

pip3 install s-tui

pip3 list

