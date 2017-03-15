tests_{1_1, 1_N, N_1, N_N} rely on ZOPKIO ( https://github.com/linkedin/Zopkio ) test framework.

Running the tests:
 - Install zopkio on the developer machine: pip install zopkio
 - run the main_test.py: zopkio --nopassword main_test.py

Some notes:
 - Zopkio is using python 2.7 (it is not recommended to use with 3.5, there are some syntax errors)
 - The target nodes are configured in the config/config.json file.
 - Zopkio deploys the tests to 192.168.1.120, .121, .122, .123 (username: riaps, password:riapspwd)
 - Discovery service is started/stopped automatically.