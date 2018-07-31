import docker
import docker.errors
import unittest

from ..agent import Agent


class AgentTest(unittest.TestCase):
    def setUp(self):
        self.containers = []
        self.docker_client = docker.from_env()

    def tearDown(self):
        for name in self.containers:
            try:
                c = self.docker_client.containers.get(name)
                c.remove(force=True)
            except docker.errors.NotFound:
                pass

    def register_cleanup(self, name):
        self.containers.append(name)

    def assertRunning(self, name):
        c = self.docker_client.containers.get(name)
        self.assertEqual(c.status, 'running')

    def assertNoContainer(self, name):
        with self.assertRaises(docker.errors.NotFound):
            self.docker_client.containers.get(name)

    def test_should_start_agent(self):
        self.register_cleanup('test_agent_1')
        agent = Agent('test_agent_1')

        agent.start()
        self.assertRunning('test_agent_1')

        agent.stop()
        self.assertNoContainer('test_agent_1')


if __name__ == '__main__':
    unittest.main()
