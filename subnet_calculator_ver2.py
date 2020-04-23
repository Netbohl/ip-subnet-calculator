#! /usr/bin/env python
"""

Example Usage:

    $ python subnet_calc.py 192.168.1.0/26

Output:
    IP Subnet Calculator
    Subnet: 192.168.0.0/26

    Netmask:   255.255.255.0 = 24
    Wildcard:  0.0.0.255

    Network:   192.168.0.0/24 (Private Internet)
    Broadcast: 192.168.0.255
    HostMin:   192.168.0.1
    HostMax:   192.168.0.254
    Hosts/Net: 254
"""
import ipaddress
import sys

def get_wildcard(netmask):
    """
    computes wildcard from netmask.

    Args:
        netmask (str):the string representation of a network mask
    Returns:
        str:the string representation of the wildcard
    """
    wildcardlist = netmask.split('.')
    wildcard = []
    for octet in wildcardlist:
        wildcard_octet = str(255 - int(octet))
        wildcard.append(wildcard_octet)
    dot = '.'
    wildcard_mask = dot.join(wildcard)
    return wildcard_mask


def pull_file():
    pass
    network_list = []
    with open('ip_networks.txt', 'r') as ip:
        for network in ip:
            network_list.append(network)
    return(network_list)



def write_output_to_file(network_object, network, notroutable, netmask, network_bits,
                wildcard_mask, network_broadcast, network_hostmin, network_hostmax, hosts_total):
    file_path = f'C:\\Users\\bohlmanc\\Subnets\\{network}.txt'
    sys.stdout = open(file_path, 'w')
    print('   IP Subnet Calculator')
    print(f'Subnet:    {network_object}\n')

    print(f'Netmask:   {netmask} = {network_bits}')
    print(f'Wildcard:  {wildcard_mask}\n')

    print(str(f'Network:   {network}') + (f' {notroutable}'))
    print(f'Broadcast: {network_broadcast}')
    print(f'Hostmin:   {network_hostmin}')
    print(f'Hostmax:   {network_hostmax}')
    print(f'Hosts/Net: {hosts_total}')
    sys.stdout.close()

def main():
    """
    Execution of the script starts here.
    this script will continually run until user hits ctrl+c or 'q'.
    """
    network_list = []
    with open('ip_networks.txt', 'r') as ip:
        for network in ip:
            network = network.rstrip('\n')
            network_list.append(network)

    for IP_network in network_list:
        
        #create network object
        network_object = ipaddress.ip_network(IP_network, strict=False)
        #wildcard/netmask
        network_bits = network_object.prefixlen
        netmask = str(network_object.netmask)
        wildcard_mask = get_wildcard(netmask)
        #broadcast
        network_broadcast = network_object.broadcast_address
        #Hosts
        all_hosts = list(network_object.hosts())
        network_hostmin = all_hosts[0]
        network_hostmax = all_hosts[-1]
        network_total = network_object.num_addresses
        hosts_total = network_total - 2
        #privte/public network
        network = network_object.network_address
        notroutable = network_object.is_private
        if notroutable == True:
            notroutable = '(Private Internet)'
        else:
            notroutable = '(Global Internet)'
        # final output
        write_output_to_file(network_object, network, notroutable, netmask, network_bits,
                        wildcard_mask, network_broadcast, network_hostmin, network_hostmax, hosts_total)

if __name__ == "__main__":
    main()
