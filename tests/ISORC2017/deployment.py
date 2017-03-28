import os

import zopkio.adhoc_deployer as adhoc_deployer
import zopkio.runtime as runtime

def setup_suite():
    # Set up authentication
    username = runtime.get_active_config("username")
    password = runtime.get_active_config("password")
    runtime.set_user(username, password)

    # Set up the target directories and properties
    userdir = os.path.join("/home", username)
    riaps_app_path = os.path.join(userdir, runtime.get_active_config("riaps_apps_path"))
    env = {"PATH": "/usr/local/bin/:$PATH",
           "RIAPSHOME": "/usr/local/riaps",
           "RIAPSAPPS": "$HOME/riaps_apps"}

    start_riaps_lang = "riaps_lang " + runtime.get_active_config('model_file')

    # Set up the sources
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              runtime.get_active_config('app_dir'),
                              runtime.get_active_config('model_file'))

    # Script to check discovery service
    discoCheckScript = "checkDiscoveryService.py"
    discoCheckScriptPath = "../test_common"
    
    # Script to start the discovery
    discoStartScript = "startDiscovery.py"
    discoStartScriptPath = "../test_common"
    
    # Script to stop the discovery
    discoStopScript = "stopDiscovery.py"
    discoStopScriptPath = "../test_common"

    killRiapsScript = "killRiaps.py"
    killRiapsScriptPath = "../test_common"

    # Deploy the riaps killer script
    for target in runtime.get_active_config('targets'):
        deployerId = "killer_" + target["host"]
        killscriptpath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), killRiapsScriptPath, killRiapsScript))

        killDeployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': killscriptpath,
            'install_path': riaps_app_path,
            'hostname': target["host"],
            "start_command": "python3 " + os.path.join(riaps_app_path, killRiapsScript)
        })
        runtime.set_deployer(deployerId, killDeployer)
        killDeployer.install(deployerId)
    

    # Deploy the riaps-disco checker script
    for target in runtime.get_active_config('targets'):
        deployerId = "disco_" + target["host"] + "_" + target["actor"]
        checkscriptpath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), discoCheckScriptPath, discoCheckScript))

        checkDiscoDeployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': checkscriptpath,
            'install_path': riaps_app_path,
            'hostname': target["host"],
            "start_command": "python3 " + os.path.join(riaps_app_path, discoCheckScript)
        })
        runtime.set_deployer(deployerId, checkDiscoDeployer)
        checkDiscoDeployer.install(deployerId)
        
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

    # Deploy the riaps-components/model file
    for target in runtime.get_active_config('targets'):
        deployerId = target["host"] + "_" + target["actor"]
        #deleteLogCommand = "rm /tmp/" + target["host"] + "*.log"
        model_deployer = adhoc_deployer.SSHDeployer(deployerId, {
            'executable': model_path,
            'install_path': os.path.join(riaps_app_path,
                                         runtime.get_active_config('app_dir')),
            'hostname': target["host"],
            'start_command': os.path.join(userdir, "/usr/local/bin/riaps_actor"),
            'args': [runtime.get_active_config('app_dir'),
                     runtime.get_active_config('app_dir') + '.json',
                     target["actor"],
                     '--address="' + target["host"]+'"'],
            'env': env,
            'terminate_only': True,
            'pid_keyword': model_path,
            'post_install_cmds': [start_riaps_lang]
        })
        runtime.set_deployer(deployerId, model_deployer)
        model_deployer.install(deployerId)

        for component in runtime.get_active_config('components_py'):
            localPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     runtime.get_active_config('app_dir'),
                                     component)
            targetPath = os.path.join(riaps_app_path, runtime.get_active_config('app_dir'))
            component_deployer = adhoc_deployer.SSHDeployer(component, {
                'executable': localPath,
                'install_path': targetPath,
                'hostname': target["host"],
                'start_command': os.path.join(userdir, "/usr/local/bin/riaps_actor"),
                'args': [runtime.get_active_config('app_dir'),
                         runtime.get_active_config('app_dir') + '.json',
                         target["actor"]],
                'env': env,
                'terminate_only': True,
                'pid_keyword': component,
            })
            runtime.set_deployer(component, component_deployer)
            component_deployer.install(component)

    print("Deployment done.")

def setup():
    print("Setup")
    # for process in server_deployer.get_processes():
    #  server_deployer.start(process.unique_id)


def teardown():
    print("Teardown")
    # for process in client_deployer.get_processes():
    #  client_deployer.stop(process.unique_id)


def teardown_suite():
    print("Teardown suite")
    # for process in model_deployer.get_processes():
    #    model_deployer.undeploy(process.unique_id)
