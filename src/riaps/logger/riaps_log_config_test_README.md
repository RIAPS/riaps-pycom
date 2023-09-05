## NAME
riaps_log_config_test -- takes a log config file as input and creates loggers to demonstrate output. Useful for checking that loggers are correctly configured.

---

### SYNOPSIS
`riaps_log_config_test` [-f FILE PATH] 
`riaps_log_config_test` [-s SPD FLAG] 

### DESCRIPTION
`riaps_log_config_test`constructs loggers from a toml file formatted that is formatted for spdlog-python for applications or the python logging framework for platform logging. The `riaps-log.conf` file for the platform is located at `/etc/riaps/riaps-log.conf` while for an application it is located in the application directory. 

#### OPTIONS
* **--help**
  + show this help message and exit
* **-F, --file**
  + Specify an alternative configuration file.  By default, riaps_log_config_test loads the configuration file from the current working directory. A platform configuration file must be in the configparser-format that is consumed by the python `logging.config.fileConfig module`. An application configuration file is in the TOML format and is consumed by the riaps [spdlog_setup script](https://github.com/RIAPS/riaps-pycom/blob/master/src/riaps/utils/spdlog_setup.py#L156) which is based on guangie88 [spdlog_setup](https://github.com/guangie88/spdlog_setup#toml-configuration-example).
* **-s, --spd**
  + Using this flag indicates an application config file that should be processed using `spdlog_setup`. If this flag is not included the config file is processed using `logging.config.fileConfig module`.






