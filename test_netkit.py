import socket
import threading
import unittest

from netkit import check_tcp, subnet_info


class TestNetKit(unittest.TestCase):
    def test_subnet_24(self):
        info = subnet_info("192.168.1.10/24")
        self.assertEqual(info["network"], "192.168.1.0")
        self.assertEqual(info["netmask"], "255.255.255.0")
        self.assertEqual(info["broadcast"], "192.168.1.255")
        self.assertEqual(info["usable_hosts"], 254)
        self.assertEqual(info["first_host"], "192.168.1.1")
        self.assertEqual(info["last_host"], "192.168.1.254")

    def test_invalid_cidr(self):
        with self.assertRaises(ValueError):
            subnet_info("not-a-network")

    def test_check_tcp_local(self):
        server = socket.socket()
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        threading.Thread(target=server.accept, daemon=True).start()
        ip, ms = check_tcp("127.0.0.1", port)
        self.assertEqual(ip, "127.0.0.1")
        self.assertGreaterEqual(ms, 0)
        server.close()


if __name__ == "__main__":
    unittest.main()
