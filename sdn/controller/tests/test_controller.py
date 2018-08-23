import unittest
import docker.types
import json
from unittest.mock import MagicMock
from ..logical_port import LogicalPort
from ..container import Container
from ..router import Router
from ..controller import Controller
from ..network import Network


class ControllerTest(unittest.TestCase):
    ROUTER_URL = "10.0.0.1"
    ROUTER_ID = "router-id"
    CONTAINER_RED_URL = "10.0.0.2"
    CONTAINER_RED_ID = "red-id"
    CONTAINER_GREEN_URL = "10.0.0.3"
    CONTAINER_GREEN_ID = "green-id"

    def test_should_post_network_to_router(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/network",
            data='{"name": "net1"}',
            headers={'content-type': 'application/json'}
        )

    def test_should_not_allow_duplicate_network_names(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        ctrl = Controller(r, MagicMock())
        n1 = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n1)

        n2 = Network("net1", "192.168.1.0/24")
        with self.assertRaises(RuntimeError):
            ctrl.add_network(n2)

    def test_should_not_allow_duplicate_network_cidrs(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        ctrl = Controller(r, MagicMock())
        n1 = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n1)

        n2 = Network("net2", "192.168.0.0/24")
        with self.assertRaises(RuntimeError):
            ctrl.add_network(n2)

    def test_should_lookup_networks_by_id(self):
        ctrl = Controller(MagicMock(), MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        stored_net = ctrl.get_network("net1")
        self.assertEqual(n, stored_net)

    def test_should_list_networks(self):
        ctrl = Controller(MagicMock(), MagicMock())
        n1 = Network('n1', '10.0.0.0/24')
        n2 = Network('n2', '10.0.1.0/24')
        ctrl.add_network(n1)
        ctrl.add_network(n2)

        networks = ctrl.list_networks()

        self.assertIn(n1, networks)
        self.assertIn(n2, networks)

    def test_should_post_logical_port_to_router(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        c = Container(self.CONTAINER_RED_ID, MagicMock(), MagicMock())
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/logical_port",
            data=json.dumps({"name": "net1", "ip": "192.168.0.2"}, sort_keys=True),
            headers={'content-type': 'application/json'}
        )

    def test_should_post_logical_port_to_container(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, MagicMock())
        c = Container(self.CONTAINER_RED_ID, poster, MagicMock())
        c.ip = self.CONTAINER_RED_URL
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with("http://"+self.CONTAINER_RED_URL + ":8090/create/logical_port",
                                       data=json.dumps({"net_id": "net1",
                                                        "net_ip": "192.168.0.0/24",
                                                        "router_ip": "192.168.0.2",
                                                        "ip": "192.168.0.3"},
                                                       sort_keys=True),
                                       headers={'content-type': 'application/json'})

    def test_should_attach_logical_port_to_network(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        c = Container(self.CONTAINER_RED_ID, MagicMock(), MagicMock())
        c.ip = self.CONTAINER_RED_URL
        docker_client = MagicMock()
        ctrl = Controller(r, docker_client)

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        mocked_network = MagicMock()
        docker_client.networks.create = MagicMock(return_value=mocked_network)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/logical_port",
            data=json.dumps({"name": "net1", "ip": "192.168.0.2"}, sort_keys=True),
            headers={'content-type': 'application/json'}
        )
        mocked_network.connect.assert_any_call(self.ROUTER_ID, ipv4_address='192.168.0.2')
        mocked_network.connect.assert_any_call(self.CONTAINER_RED_ID, ipv4_address='192.168.0.3')

    def test_should_list_logical_ports(self):
        ctrl = Controller(MagicMock(), MagicMock())
        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)
        c1 = Container(self.CONTAINER_RED_ID, MagicMock(), MagicMock())
        c2 = Container(self.CONTAINER_GREEN_ID, MagicMock(), MagicMock())
        p1 = LogicalPort(c1, n)
        p2 = LogicalPort(c2, n)
        ctrl.add_logical_port(p1)
        ctrl.add_logical_port(p2)

        ports = ctrl.list_logical_ports()

        self.assertIn(p1, ports)
        self.assertIn(p2, ports)

    def test_should_start_containers(self):
        docker_client = MagicMock()
        ctrl = Controller(MagicMock(), docker_client)
        ctrl.add_container('container-id', 'sdn')

        docker_client.containers.run.assert_called()

    def test_should_stop_containers(self):
        container_mock = MagicMock()
        docker_client = MagicMock()
        docker_client.containers.get = MagicMock(return_value=container_mock)
        ctrl = Controller(MagicMock(), docker_client)
        ctrl.add_container('container-id', 'sdn')
        ctrl.remove_container('container-id')

        container_mock.remove.assert_called()
        self.assertEqual(ctrl.containers, {})

    def test_should_lookup_containers_by_id(self):
        ctrl = Controller(MagicMock(), MagicMock())
        ctrl.add_container('container-id', 'sdn')

        container = ctrl.get_container('container-id')

        self.assertEqual(container.id, 'container-id')

    def test_clean(self):
        ctrl = Controller(MagicMock(), MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        self.assertEqual(n, ctrl.networks['net1'])
        self.assertNotEqual(ctrl.ipam_pools['net1'], {})

        ctrl.clean()

        self.assertEqual(ctrl.networks, {})

    def test_should_remove_containers_when_cleaned(self):
        container_mock = MagicMock()
        docker_client = MagicMock()
        docker_client.containers.get = MagicMock(return_value=container_mock)
        ctrl = Controller(MagicMock(), docker_client)
        ctrl.add_container('container-id', 'sdn')

        ctrl.clean()

        container_mock.remove.assert_called()

    def test_should_list_containers(self):
        ctrl = Controller(MagicMock(), MagicMock())
        ctrl.add_container('c1', 'sdn')
        ctrl.add_container('c2', 'sdn')

        containers = ctrl.list_containers()

        self.assertIn(Container('c1', MagicMock(), MagicMock()), containers)
        self.assertIn(Container('c2', MagicMock(), MagicMock()), containers)


if __name__ == '__main__':
    unittest.main()
