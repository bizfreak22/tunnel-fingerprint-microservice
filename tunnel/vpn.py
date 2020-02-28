#!/usr/bin/env python3

from p0f import P0f, P0fException

_MISC_TUNNEL_VALUES = ['gif', 'vpn', 'ipsec', 'ipip', 'pptp']
DEFAULT_P0F_SOCKET_PATH = '/var/run/p0f.sock'

def _decodeBytes(byte_str):
    """ Decode bytes and stripping out null characters """
    return byte_str.decode('utf-8').rstrip('\x00')

def _lookup(query, p0f_socket_path):
    """ Queries data from named p0f socket """ 
    data = None
    p0f_socket = P0f(p0f_socket_path)
    try:
        data = p0f_socket.get_info(query, True) # disable validation
    except P0fException:
        pass
    except KeyError:
        pass
    except ValueError:
        pass
    finally:
        p0f_socket.close()
    return data

def is_generic_vpn(ip, p0f_socket_path = DEFAULT_P0F_SOCKET_PATH, debug = False):
    """ Checks if ip is using a generic protocol """
    results = _lookup(ip, p0f_socket_path)
    if results:
        if debug:
            print(results)
        # Target link type based on MTU signature
        if 'link_type' in results and results['link_type'] != None:
            link_type = _decodeBytes(results['link_type']).lower()
            if debug:
                print(link_type)
            for v in _MISC_TUNNEL_VALUES:
                if v in link_type:
                    return True
        # Target mismatched OS and software stack signatures (i.e Safari on Linux)
        if 'bad_sw' in results and results['bad_sw'] != None:
            bad_sw = results['bad_sw']
            if debug:
                print(str(bad_sw))
            return bad_sw > 0 # possible proxy or os mismatch from UA spoof
    return False
