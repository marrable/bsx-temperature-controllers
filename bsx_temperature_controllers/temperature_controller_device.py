from ophyd import PVPositioner, EpicsSignal, EpicsSignalRO, Component


class TemperatureControllerDevice(PVPositioner):
    setpoint = Component(EpicsSignal, 'TARGET_TEMP')
    readback = Component(EpicsSignalRO, 'SAMPLE_TEMP')
    actuate = Component(EpicsSignal, 'ACTUATE_CONTROLLER')
    
    stop_signal = Component(EpicsSignal, 'STOP_CONTROLLER')
    
    done = Component(EpicsSignalRO, 'DONE_CONTROLLER')
    
    ramp_rate = Component(EpicsSignal, 'RAMP_RATE')

    _default_read_attrs = ['readback', 'setpoint']
