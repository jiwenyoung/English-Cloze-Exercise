from abc import ABC,abstractmethod

class Origin(ABC):
    
    @abstractmethod
    def pull(self):
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    @abstractmethod
    def clean(self):
        raise NotImplementedError

    @abstractmethod
    def filter(self):
        raise NotImplementedError

    @abstractmethod
    def output(self):
        raise NotImplementedError