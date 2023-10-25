from pathlib import Path

from caproto.server import ioc_arg_parser, run

from bsx_temperature_controllers.temperature_controller_ioc import TemperatureControllerIOC
from bsx_temperature_controllers.linkam.linkam_controller import LinkamController


SDK_ROOT_PATH = r"C:\Users\admin\Projects\TestingPyLinkam\testing-pylinkam\.venv\Lib\site-packages\pylinkam"
SDK_LICENSE_PATH = r"C:\Users\admin\Projects\TestingPyLinkam\testing-pylinkam\.venv\Lib\site-packages\pylinkam\Linkam.lsk"
SDK_LOG_PATH = str(Path.cwd() / Path("Linkam.log"))

DEFAULT_TOLERANCE = 0.02
DEFAULT_RAMP_RATE = 10.0 # K/s
DEFAULT_DWELL_TIME = 1800.0 # s = half an hour
DEFAULT_LOW_TEMPERATURE = -201
DEFAULT_HIGH_TEMPERATURE = 350
DEFAULT_LOW_RAMP_RATE = 0
DEFAULT_HIGH_RAMP_RATE = 29.99

def run_ioc():
    linkam_controller = LinkamController(
        sdk_root_path=SDK_ROOT_PATH,
        sdk_log_path=SDK_LOG_PATH,
        sdk_license_path=SDK_LICENSE_PATH,
        tolerance=DEFAULT_TOLERANCE,
        dwell_time=DEFAULT_DWELL_TIME,
        temperture_limits=(DEFAULT_LOW_TEMPERATURE, DEFAULT_HIGH_TEMPERATURE),
        ramp_limits=(DEFAULT_LOW_RAMP_RATE, DEFAULT_HIGH_RAMP_RATE)
    )

    ioc_options, run_options = ioc_arg_parser(
        default_prefix='BSX-LINKAM:',
        desc="Linkam IOC",
    )
    
    ioc = TemperatureControllerIOC(temperature_controller=linkam_controller, **ioc_options)
    ioc.sleep = 0.2
    run(ioc.pvdb, **run_options)


if __name__ == "__main__":
    run_ioc()
