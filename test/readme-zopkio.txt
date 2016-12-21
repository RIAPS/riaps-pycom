tests_{1_1, 1_N, N_1, N_N} rely on ZOPKIO ( https://github.com/linkedin/Zopkio ) test framework.

Running the tests:
 - Install zopkio: pip install zopkio
 - run the main_test.py: zopkio --nopassword main_test.py

Some notes:
 - Zopkio is using python 2.7 (it is not recommended to use with 3.5, because there are syntax errors)
 - The target hardware(s) is configured in the config/config.json file. Now zopkio is configured to deploy the tests to 192.168.1.104 (ubuntu/temppwd)
 - Discovery service is not started automatically. Before the test, start the discovery service on the target machine.