import os

import zopkio.adhoc_deployer as adhoc_deployer
import zopkio.runtime as runtime


def setup_suite():
    runtime.set_user("ubuntu", "temppwd")
    # client_exec = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                           "AdditionClient/out/artifacts/AdditionClient_jar/AdditionClient.jar")

    # current_dir = os.path.dirname(__file__)


    local_estimator_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'DistributedEstimator/LocalEstimator.py')

    global local_estimator_deployer
    local_estimator_deployer = adhoc_deployer.SSHDeployer("localestimator", {
        'executable': local_estimator_path,
        'install_path': "/home/ubuntu/riaps_apps",
        'hostname': "192.168.1.104",
        'start_command': "riaps_actor",
        'args': "DistributedEstimator DistributedEstimator.json Estimator",
        'terminate_only': True,
        'pid_keyword': "localEstimator"
    })

    runtime.set_deployer("localestimator", local_estimator_deployer)

    local_estimator_deployer.install("localestimator",
                                     {"hostname": "192.168.1.104",
                                      "install_path": "/home/ubuntu/riaps_apps"})


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
    # for process in server_deployer.get_processes():
    #  server_deployer.undeploy(process.unique_id)
