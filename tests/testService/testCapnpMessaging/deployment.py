import os, sys, inspect

import zopkio.adhoc_deployer as adhoc_deployer
import zopkio.runtime as runtime
from time import sleep

def setup_suite():
    # Set up authentication
    username = runtime.get_active_config("username")
    password = runtime.get_active_config("password")
    runtime.set_user(username, password)

    # Set up the target directories and properties
    userdir = os.path.join("/home", username)
    riaps_app_path = os.path.join(userdir, runtime.get_active_config("riaps_apps_path"))

    # Script to check discovery service
    discoCheckScript = "checkDiscoveryService.py"
    discoCheckScriptPath = "../../test_common"

    # Script to start the discovery
    discoStartScript = "startDiscovery.py"
    discoStartScriptPath = "../../test_common"

    # Script to stop the discovery
    discoStopScript = "stopDiscovery.py"
    discoStopScriptPath = "../../test_common"

    testCapnpMessagingScript = "testCapnpMessaging.py"

    env = {"PATH": "~/.local/bin/:$PATH",
           "RIAPSHOME": "$HOME/.local/riaps",
           "RIAPSAPPS": "$HOME/riaps_apps"}

    # Deploy the discovery starter script
    for target in runtime.get_active_config('targets'):
        deployerId = "discostart_" + target["host"]
        startscriptpath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), discoStartScriptPath, discoStartScript))

        startDiscoveryDeployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': startscriptpath,
            'install_path': riaps_app_path,
            'hostname': target["host"],
            "start_command": "python3 " + os.path.join(riaps_app_path, discoStartScript)
        })
        runtime.set_deployer(deployerId, startDiscoveryDeployer)
        startDiscoveryDeployer.install(deployerId)

    # Deploy the discovery stop script
    for target in runtime.get_active_config('targets'):
        deployerId = "discostop_" + target["host"]
        stopscriptpath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), discoStopScriptPath, discoStopScript))

        stopDiscoveryDeployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': stopscriptpath,
            'install_path': riaps_app_path,
            'hostname': target["host"],
            "start_command": "python3 " + os.path.join(riaps_app_path, discoStopScript)
        })
        runtime.set_deployer(deployerId, stopDiscoveryDeployer)
        stopDiscoveryDeployer.install(deployerId)

    # Deploy the riaps-disco checker script
    for target in runtime.get_active_config('targets'):
        deployerId = "disco" + target["host"]
        checkscriptpath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), discoCheckScriptPath, discoCheckScript))

        checkDiscoDeployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': checkscriptpath,
            'install_path': riaps_app_path,
            'hostname': target["host"],
            "start_command": "python3 " + os.path.join(riaps_app_path, "checkDiscoveryService.py")
        })
        runtime.set_deployer(deployerId, checkDiscoDeployer)
        checkDiscoDeployer.install(deployerId)

    # Deploy the additional files + test script
    for target in runtime.get_active_config('targets'):
        localPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 runtime.get_active_config('app_dir'),
                                 testCapnpMessagingScript)
        messaging_deployer = adhoc_deployer.SSHDeployer(target["host"], {
            'executable': localPath,
            'install_path': os.path.join(riaps_app_path,
                                         runtime.get_active_config('app_dir')),
            'hostname': target["host"],
            'env': env,
            'start_command': "python3",
            'args': [os.path.join(riaps_app_path, runtime.get_active_config('app_dir'), testCapnpMessagingScript),
                     target["host"]+'.log'],
            'terminate_only': True,
        })
        runtime.set_deployer(target["host"], messaging_deployer)
        messaging_deployer.install(target["host"])

        for f in runtime.get_active_config('additionalFiles'):
            localPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     runtime.get_active_config('app_dir'),
                                     f)
            targetPath = os.path.join(riaps_app_path, runtime.get_active_config('app_dir'))
            file_deployer = adhoc_deployer.SSHDeployer(f, {
                'executable': localPath,
                'install_path': targetPath,
                'hostname': target["host"],
                'start_command': os.path.join(userdir, ".local/bin/riaps_actor"),
                'terminate_only': True,
                'pid_keyword': f,
            })
            runtime.set_deployer(f, file_deployer)
            file_deployer.install(f)

    print("Deployment done.")

def reach_discovery():
    for target in runtime.get_active_config("targets"):
        deployerId = "disco" + target["host"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})

def setup():
    print("Start discovery service...")

    started_hosts = set()

    # Start discovery
    for target in runtime.get_active_config("targets"):
        deployerId = "discostart_" + target["host"]
        if deployerId not in started_hosts:
            started_hosts.add(deployerId)
            deployer = runtime.get_deployer(deployerId)
            deployer.start(deployerId, configs={"sync": False})
    sleep(2)

    reach_discovery()

    #print("Setup")
    # for process in server_deployer.get_processes():
    #  server_deployer.start(process.unique_id)


def teardown():


    print("Stop discovery...")
    # Stop discovery
    for target in runtime.get_active_config("targets"):
        deployerId = "discostop_" + target["host"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})
    sleep(10)
    print(" -- END -- ")

    # for process in client_deployer.get_processes():
    #  client_deployer.stop(process.unique_id)


def teardown_suite():
    print("Teardown suite")
    # for process in model_deployer.get_processes():
    #    model_deployer.undeploy(process.unique_id)
