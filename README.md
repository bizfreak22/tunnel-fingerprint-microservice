# tunnel-fingerprint-microservice

Simple microservice to detect generic tunneling protocols like OpenVPN, Wireguard or older protocols like IPSec from a single TCP/UDP connection. Additionally checks for Tor as a fallback.

# Usage
  Requires [p0f3](http://lcamtuf.coredump.cx/p0f3/) to be installed and running as a daemon with a named unix socket. See p0f instructions for details.
  
  ## Sample non-docker install
    git clone https://github.com/idealwebsolutions/tunnel-fingerprint-microservice
    cd tunnel-fingerprint-microservice
    pip install pipenv gunicorn
    pipenv shell
    pipenv install
    gunicorn -b 0.0.0.0:8080 main:app
  ## Sample docker install (recommended)
    docker pull https://github.com/idealwebsolutions/tunnel-fingerprint-microservice
    docker build -t "tunnel-fingerprint-microservice" .
    docker run -d --name="fingerprint-microservice" \
     -v /path/to/named/p0f/socket:/var/run/ -p 8080:80 tunnel-fingerprint-microservice

# API
## /fingerprint?ip=MY.IP.V4.ADDRESS
Takes in a valid IPv4 address and returns two fields indicating if a VPN or Tor was identified.
```json
{
    "is_vpn": True,
    "is_tor": False
}
```

# Support
Detection methods used rely on specific MTU values and guesses based on OS and software stack signature mismatches; this is not a reliable method due to wide array of configurations out there and the ability to spoof the user-agent header. However with some refinement and testing, it may cover a good portion of generic configurations out there.

# Tested VPN services
- Mullvad (OpenVPN and Wireguard)
- ProtonVPN

# License
MIT