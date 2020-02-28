#!/usr/bin/env python3

from dns import resolver, exception

# https://2019.www.torproject.org/projects/tordnsel.html.en

_DEFAULT_DEST_IP = '216.58.206.110' # Google
_DEFAULT_EXIT_PORT = 443
_DEFAULT_TOR_DNS = 'ip-port.exitlist.torproject.org'

def _reverse_ip(ip):
    """ Reverses IPv4 address string """
    return '.'.join(ip.split('.')[::-1])

def _lookup(query, attempts = 3):
    """ Looks up a DNS query on tordnsel """
    answers = []
    # Return if no answers found after three attempts 
    if attempts == 0:
        return answers
    try:
        answers = resolver.query(query)
    except exception.Timeout:
        return lookup(query, attempts - 1)
    except exception.DNSException:
        pass
    return answers

def is_exit_node(ipv4, port = _DEFAULT_EXIT_PORT, debug = False):
    """ Determines if ipv4 address is a tor exit node """
    reversed_ip = _reverse_ip(ipv4)
    # If provided ipv4 is not a valid address raise error
    if reversed_ip is None:
        raise ValueError('Invalid IPv4 address provided')
    # Iterate through addresses to see if one matches special address
    for answer in _lookup('{}.{}.{}.{}'.format(reversed_ip, port, _reverse_ip(_DEFAULT_DEST_IP), _DEFAULT_TOR_DNS)):
        if debug:
            print(answer)
        if str(answer) == '127.0.0.2':
            return True
    # Return false if no answers found or does not match special address
    return False
