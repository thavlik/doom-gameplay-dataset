# https://unix.stackexchange.com/questions/182220/route-everything-through-vpn-except-ssh-on-port-22
ip rule add table 128 from 165.22.34.206
ip route add table 128 to 165.22.34.0/24 dev eth0
ip route add table 128 default via 165.22.32.1