#!/usr/bin/env python3

from os import getenv
from falcon import API, HTTPBadRequest
from json import dumps

from tunnel.tor import is_exit_node
from tunnel.vpn import is_generic_vpn, DEFAULT_P0F_SOCKET_PATH

def _is_valid_ipv4_format(ip):
    return len(ip.split('.')) == 4

class TunnelFingerprint:
  def on_get(self, req, res):
    """ Handles fingerprinting ip as either generic VPN or Tor Exit Node """
    ip = req.get_param('ip')
    if not ip:
      raise HTTPBadRequest('Missing parameter IP', 'Request must include IP parameter')
    if not _is_valid_ipv4_format(ip):
      raise HTTPBadRequest('Invalid IPv4 address', 'IP address must be a valid ipv4 format')
    # Check if connection is using a vpn protocol or tor
    res.body = dumps({
      'is_vpn': is_generic_vpn(ip, getenv('p0f_sock_path', DEFAULT_P0F_SOCKET_PATH)),
      'is_tor': is_exit_node(ip)
    })

app = API()
app.add_route('/fingerprint', TunnelFingerprint())
