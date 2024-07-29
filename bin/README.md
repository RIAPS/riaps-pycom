# Eclipse External Tool Launch Files

If using eclipse to work on RIAPS application development, there are several external tool launch files available to run the RIAPS framework tools.  
These tools can be imported into the eclipse environment using "Run/Debug" and "Launch Configurations" options in the "Import Wizard".  When
importing these launch configurations, the "Build before launch" flag is automatically checked under the "Build" tab of the configuration.  ***Make
sure to uncheck this option.***

- riaps_ctrl.launch:  starts the RIAPS controller
- riaps_deplo.launch:  starts the RIAPS deployment manager on the host environment
- rpyc_registry.launch:  starts the background rpyc_registry tool used by the RIAPS Controller.  This external tool is no longer necessary since this is automatically started using systemd on the development environment where the controller will be run.  It is available here in case it is desired to be run manually instead of in the background.
