from abc import abstractmethod

class VPN:
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    def reconnect(self):
        self.disconnect()
        self.connect()

