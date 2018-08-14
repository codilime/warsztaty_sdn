import unittest
from ..network import Network


class NetworkTests(unittest.TestCase):
    def test_should_compare_by_id(self):
        same1 = Network("net1", "192.168.0.0/24")
        same2 = Network("net1", "")
        other = Network("net2", "192.168.0.0/24")

        self.assertEqual(same1, same2)
        self.assertNotEqual(same1, other)


if __name__ == '__main__':
    unittest.main()
