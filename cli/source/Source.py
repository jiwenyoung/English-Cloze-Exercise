from abc import ABC,abstractmethod

class Source(ABC):
    
    @abstractmethod
    def collect(self):
        raise NotImplementedError

    @abstractmethod
    def fetch(self):
        raise NotImplementedError

    @abstractmethod
    def save(self):
        raise NotImplementedError

    @abstractmethod
    def output(self):
        raise NotImplementedError
