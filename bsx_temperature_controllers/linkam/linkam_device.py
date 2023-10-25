#%%
import time

from bsx_temperature_controllers.temperature_controller_device import TemperatureControllerDevice



def linkam_factory(): 
    linkam = TemperatureControllerDevice('BSX-LINKAM:')
    linkam.ramp_rate.put(10.0)
    return linkam


if __name__ == "__main__":
    linkam = linkam_factory()
    linkam.move(30, wait=False)
    while not linkam.done.get() == linkam.done_value:
        time.sleep(1.0)
        print(linkam.get())
        

    for i in range(30):
        time.sleep(1.0)
        print(i, linkam.get())

    linkam.stop_signal.put(linkam.stop_value, wait = True)
    time.sleep(1.0)
    print(linkam.get())
    

    
# %%
