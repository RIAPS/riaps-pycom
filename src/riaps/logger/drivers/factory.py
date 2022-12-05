
import riaps.logger.drivers.tmux_driver as tmux_driver
import riaps.logger.drivers.console_driver as console_driver
import riaps.logger.drivers.file_driver as file_driver

def get_driver(driver_type, **kwargs):
    drivers = {
        "tmux" : tmux_driver.ServerLogDriver,
        "console" : console_driver.ServerLogDriver,
        "file" : file_driver.ServerLogDriver
        }
    driver_class = drivers.get(driver_type,None)
    return driver_class(driver_type, **kwargs) \
        if driver_class else  console_driver.ServerLogDriver (driver_type, **kwargs)

    
