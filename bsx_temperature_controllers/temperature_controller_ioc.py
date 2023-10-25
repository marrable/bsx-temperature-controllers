#%%


from caproto.server import pvproperty, PVGroup

from bsx_temperature_controllers.temperature_controller import TemperatureController

TRUE_FALSE_DICT = {'On': True, 'Off': False, True: True, False: False, 1: True, 0: False}
SLEEP_TIME = 1.1


class TemperatureControllerIOC(PVGroup):
    sleep = SLEEP_TIME
    sample_temperature = pvproperty(name = 'SAMPLE_TEMP', value = 0.0, record='ai', doc = 'documentation')
    target_temperature = pvproperty(name = 'TARGET_TEMP', value = 0.0, record='ao', doc = 'documentation')
    actuate_controller = pvproperty(name = 'ACTUATE_CONTROLLER', value = False, record = 'bo', doc = 'documentation')
    done_controller = pvproperty(name = 'DONE_CONTROLLER', value = False, record = 'bi', doc = 'documentation')
    stop_controller = pvproperty(name = 'STOP_CONTROLLER', value = False, record = 'bo', doc = 'documentation')

    ramp_rate = pvproperty(name = 'RAMP_RATE', value = 0.0, record = 'ao', doc = 'documentation' )

    update_hook = pvproperty(name="_update", value=False, record='bi')


    def set_temperature_controller(self, temperature_controller: TemperatureController):
        self.temperature_controller = temperature_controller

    def __init__(self, *args, temperature_controller: TemperatureController, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_temperature_controller(temperature_controller)

    async def update_pvproperties(self):
        await self.sample_temperature.write(value = self.temperature_controller.get_current_temperature())
        await self.done_controller.write(value = self.temperature_controller.done_controller())

    @sample_temperature.startup
    async def sample_temperature(self, instance, async_lib):
        self.temperature_controller.connect()
        await self.sample_temperature.write(value=self.temperature_controller.get_current_temperature())
        await self.target_temperature.write(value=self.temperature_controller.get_target_temperature())
        
        await self.ramp_rate.write(value = self.temperature_controller.get_ramp_rate())
        
    @update_hook.scan(period=0.01, use_scan_field=True)
    async def update_hook(self, instance, async_lib):
        await async_lib.library.sleep(self.sleep)
        await self.update_pvproperties()

    @actuate_controller.putter
    async def actuate_controller(self, instance, value):
        b = TRUE_FALSE_DICT[value]
        if b:
            self.temperature_controller.start_heating(self.target_temperature.value, self.ramp_rate.value)
        return False

    @actuate_controller.shutdown
    async def actuate_controller(self, instance, async_lib):
        await self.stop_controller.write(value = True)
        self.temperature_controller.close()
        await async_lib.library.sleep(self.sleep)

    @target_temperature.putter
    async def target_temperature(self, instance, value):
        temperature_low_limit, temperature_high_limit = self.temperature_controller.get_temperature_limits()
        if not (temperature_low_limit <= value <= temperature_high_limit):
            raise ValueError(f"Target temperature setpoint should be in range between {temperature_low_limit} and {temperature_high_limit}")
        return value

    @ramp_rate.putter
    async def ramp_rate(self, instance, value):
        ramp_low_limit, ramp_high_limit = self.temperature_controller.get_ramp_limits()
        if not (ramp_low_limit <= value <= ramp_high_limit):
            raise ValueError(f"Target temperature setpoint should be in range between {ramp_low_limit} and {ramp_high_limit}")
        return value
    
    @stop_controller.putter
    async def stop_controller(self, instance, value):
        b = TRUE_FALSE_DICT[value]
        if b:
            self.temperature_controller.stop_controller()
        return False

