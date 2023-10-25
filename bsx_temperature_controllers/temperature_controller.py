#%%

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class TemperatureController(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass    

    @abstractmethod
    def get_current_temperature(self) -> float:
        pass

    @abstractmethod
    def get_target_temperature(self) -> float:
        pass

    @abstractmethod
    def get_ramp_rate(self) -> float:
        return 0.0
    
    @abstractmethod
    def get_temperature_limits(self) -> tuple[float, float]:
        pass
    
    @abstractmethod
    def get_ramp_limits(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def done_controller(self) -> bool:
        pass

    @abstractmethod
    def stop_controller(self) -> None:
        pass

    @abstractmethod
    def start_heating(self, target_temperature: float, ramp_rate: float = 0.0) -> None:
        pass

    