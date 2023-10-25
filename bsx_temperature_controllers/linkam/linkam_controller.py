from dataclasses import dataclass, field
from typing import Optional, Any

import numpy as np
import pint

from pylinkam import interface, sdk

from bsx_temperature_controllers.temperature_controller import TemperatureController

DEFAULT_TOLERANCE = 0.02
DEFAULT_RAMP_RATE = 10.0 # K/s
DEFAULT_DWELL_TIME = 1800.0 # s = half an hour
DEFAULT_LOW_TEMPERATURE = -201
DEFAULT_HIGH_TEMPERATURE = 350
DEFAULT_LOW_RAMP_RATE = 0
DEFAULT_HIGH_RAMP_RATE = 29.99

@dataclass
class LinkamController(TemperatureController):
    sdk_root_path: str
    sdk_log_path: Optional[str] = None
    sdk_license_path: Optional[str] = None
    debug: bool = False
    # use_serial: bool = False # Use of USB is hard-coded in this class. A serial implementation should be its own class
    tolerance: float = DEFAULT_TOLERANCE
    dwell_time: float = DEFAULT_DWELL_TIME
    temperture_limits: tuple[float, float] = field(default_factory= lambda : (DEFAULT_LOW_TEMPERATURE, DEFAULT_HIGH_TEMPERATURE))
    ramp_limits: tuple[float, float] = field(default_factory=lambda  : (DEFAULT_LOW_RAMP_RATE, DEFAULT_HIGH_RAMP_RATE))
    _handle: sdk.SDKWrapper = None
    

    def connect(self) -> None:
        self._handle = sdk.SDKWrapper(
            sdk_root_path=self.sdk_root_path,
            sdk_log_path=self.sdk_log_path,
            sdk_license_path=self.sdk_license_path,
            debug=self.debug
        )
        self._connection = self._handle._connect_usb()

    def close(self) -> None:
        self._connection.close()
        self._handle.close()
        self._handle = None

    def get_value(self, interface_type: interface.StageValueType) -> float:
        value = self._connection.get_value(interface_type)
        if isinstance(value, pint.Quantity):
            return value.magnitude
        return value
    
    def set_value(self, interface_type: interface.StageValueType, value: Any) -> None:
        self._connection.set_value(interface_type, value)

    def enable_heating(self, heater_enabled: bool) -> None:
        self._connection.enable_heater(heater_enabled)

    def get_current_temperature(self) -> float:
        return self.get_value(interface.StageValueType.HEATER1_TEMP)
    
    def get_target_temperature(self) -> float:
        return self.get_value(interface.StageValueType.HEATER_SETPOINT)
    
    def get_ramp_rate(self) -> float:
        return self.get_value(interface.StageValueType.HEATER_RATE)
    
    def get_dwell_time(self) -> float:
        return self.get_value(interface.StageValueType.RAMP_HOLD_REMAINING)
    
    def get_temperature_limits(self) -> tuple[float, float]:
        return self.temperture_limits
    
    def get_ramp_limits(self) -> tuple[float, float]:
        return self.ramp_limits
    
    def done_controller(self) -> bool:
        if np.abs(self.get_current_temperature() - self.get_target_temperature()) > self.tolerance:
            return False
        return self.get_value(interface.StageValueType.RAMP_HOLD_REMAINING) > 0.01 # Remain ramp time less than zero means heater is off
    
    def stop_controller(self) -> None:
        self.enable_heating(False)
    
    def start_heating(self, target_temperature: float, ramp_rate: float = 0) -> None:
        connection = self._connection
        connection.set_value(interface.StageValueType.HEATER_SETPOINT, target_temperature)
        connection.set_value(interface.StageValueType.HEATER_RATE, ramp_rate if ramp_rate != 0 else DEFAULT_RAMP_RATE)
        connection.set_value(interface.StageValueType.RAMP_HOLD_TIME, self.dwell_time)
        connection.enable_heater(True)
