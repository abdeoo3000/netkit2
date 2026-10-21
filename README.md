# 🌐 NetKit

A small command-line networking toolkit written in Python.

## Description

NetKit bundles two handy networking tools in one script:

- **Subnet calculator** – enter a network in CIDR notation and get the network address,
  netmask, broadcast address, number of usable hosts, and first/last host.
- **TCP connectivity check** – test whether a host is reachable on a given TCP port and
  measure the connection latency.

It uses only Python's standard library (`ipaddress`, `socket`), so there is nothing to install.

## Installation

Requirements: [Python 3.8+](https://www.python.org/downloads/)

```bash
git clone https://github.com/abdeoo3000/netkit.git
cd netkit
```

## Usage Example

Calculate a subnet:

```bash
python netkit.py subnet 192.168.1.10/24
```

```
         network: 192.168.1.0
         netmask: 255.255.255.0
          prefix: 24
       broadcast: 192.168.1.255
 total_addresses: 256
    usable_hosts: 254
      first_host: 192.168.1.1
       last_host: 192.168.1.254
```

Check whether a port is reachable:

```bash
python netkit.py check example.com 443
# OPEN  example.com (93.184.216.34) port 443 - 41.7 ms
```

Run the tests:

```bash
python -m unittest
```

> Only test hosts and networks that you own or have permission to test.

## Contributor Credits

- **Abdallah Anwer Abdallah** – author & maintainer ([@abdeoo3000](https://github.com/abdeoo3000))

Contributions are welcome! Fork the repo, create a branch, and open a pull request.

## License

Released under the [MIT License](LICENSE).
