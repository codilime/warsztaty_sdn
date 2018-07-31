import docker


class Agent(object):
    def __init__(self, name):
        self.__name = name
        self.__containter = None

    def start(self):
        client = docker.from_env()
        self.__containter = client.containers.run('sdn-agent', name=self.__name, detach=True, remove=True)

    def stop(self):
        self.__containter.stop()