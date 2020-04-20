#! /usr/bin/env python
"""
This script is a part of a tutorial to build a Python subnet Calculator.

The script accepts string inputs in the following formats:
`192.168.1.0/24` or `192.168.2.0/255.255.255.0`

Example Usage:

    $ python subnet_calc.py 192.168.1.0/26

Output:
    IP Subnet Calculator
    Subnet: 192.168.0.0/26

    Network:   192.168.0.0/24 (Private Internet)
    Netmask:   255.255.255.0 = 24
    Wildcard:  0.0.0.255

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


def prompt_user():
    """
    prompts the user for network and returns the input.
    """
    try:
        IP_network = input(' \n'
                                '-------------------------------------------------------------------------\n'
                                'Enter the network address in the one of following formats or "q" to quit.\n'
                                'Network/CIDR - 192.168.1.0/24\n'
                                'Network/Subnet - 192.168.1.0/255.255.255.0\n'
                                '---------\n'
                                'Network: ')
        if IP_network.lower() == 'q':
            # break # break out of loop
            sys.exit('User quit Subnet Calculator')
        else:
            return IP_network
    except KeyboardInterrupt:
        print('Thanks for using IP subnet calculator')


def main(cli_args):
    """
    Execution of the script starts here.
    this script will continually run until user hits ctrl+c or 'q'.
    """
    
    while True:
        cli_args_exist = False
        if len(cli_args) > 1:
            cli_args_exist = True
            IP_network = cli_args[1]
        else:
            IP_network = prompt_user()

        try:
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

            print('_________________________________________')
            print(' ')
            print('   IP Subnet Calculator')
            print(f'Subnet:    {network_object}\n')
            
            print(str(f'Network:   {network}') + (f' {notroutable}'))
            print(f'Netmask:   {netmask} = {network_bits}')
            print(f'Wildcard:  {wildcard_mask}\n')
            
            print(f'Broadcast: {network_broadcast}')
            print(f'Hostmin:   {network_hostmin}')
            print(f'Hostmax:   {network_hostmax}')
            print(f'Hosts/Net: {hosts_total}')
            print(' ')
            if cli_args_exist:
                sys.exit()
        except ValueError:
            print('Be sure to enter IP address in the proper format')
            continue
        #except:
        #    print(f'{IP_network} is not a valid network\n'
        #   'please enter again using the proper format')
    
    print('User quit Subnet Calculator')
    
if __name__ == "__main__":
    args = sys.argv
    main(args)
