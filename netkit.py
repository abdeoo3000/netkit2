"""NetKit - small networking toolkit: subnet calculator and TCP connectivity check."""
import argparse
import ipaddress
import socket
import time


def subnet_info(cidr):
    """Return a dict with details about an IPv4/IPv6 network in CIDR notation."""
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = list(net.hosts()) if net.num_addresses <= 65536 else None
    info = {
        "network": str(net.network_address),
        "netmask": str(net.netmask),
        "prefix": net.prefixlen,
        "broadcast": str(net.broadcast_address) if net.version == 4 else "n/a",
        "total_addresses": net.num_addresses,
        "usable_hosts": max(net.num_addresses - 2, 0) if net.version == 4 and net.prefixlen < 31
        else net.num_addresses,
    }
    if hosts:
        info["first_host"] = str(hosts[0])
        info["last_host"] = str(hosts[-1])
    return info


def check_tcp(host, port, timeout=3.0):
    """Try to open a TCP connection. Returns (ip, latency_ms) or raises OSError."""
    ip = socket.gethostbyname(host)
    start = time.perf_counter()
    with socket.create_connection((ip, port), timeout=timeout):
        pass
    return ip, (time.perf_counter() - start) * 1000


def main():
    parser = argparse.ArgumentParser(description="Small networking toolkit.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sub = sub.add_parser("subnet", help="calculate subnet details from CIDR")
    p_sub.add_argument("cidr", help="e.g. 192.168.1.0/24")

    p_chk = sub.add_parser("check", help="check if a TCP port is reachable")
    p_chk.add_argument("host", help="hostname or IP, e.g. example.com")
    p_chk.add_argument("port", type=int, help="TCP port, e.g. 443")
    p_chk.add_argument("-t", "--timeout", type=float, default=3.0)

    args = parser.parse_args()

    if args.command == "subnet":
        try:
            for key, value in subnet_info(args.cidr).items():
                print(f"{key:>16}: {value}")
        except ValueError as err:
            print(f"Invalid network: {err}")
    else:
        try:
            ip, ms = check_tcp(args.host, args.port, args.timeout)
            print(f"OPEN  {args.host} ({ip}) port {args.port} - {ms:.1f} ms")
        except (OSError, socket.timeout) as err:
            print(f"CLOSED/UNREACHABLE  {args.host}:{args.port} - {err}")


if __name__ == "__main__":
    main()
