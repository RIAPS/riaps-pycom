import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep

def test_pub_sub():

    #Start discovery
    for target in runtime.get_active_config("targets"):
        deployerId = "discostart_" + target["host"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": False})
    sleep(10)

    # Test if disco is avaliable
    for target in runtime.get_active_config("targets"):
        deployerId = "disco_" + target["host"] + "_" + target["actor"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})

    # start the test
    for target in runtime.get_active_config("targets"):
        if target["actor"]=="ActorCollector":
            deployerId = target["host"] + "_" + target["actor"]
            deployer = runtime.get_deployer(deployerId)
            deployer.start(target["actor"], configs={"sync": False})

    sleep(10)

    # start the test
    for target in runtime.get_active_config("targets"):
        if target["actor"] == "ActorSensor":
            deployerId = target["host"] + "_" + target["actor"]
            deployer = runtime.get_deployer(deployerId)
            deployer.start(target["actor"], configs={"sync": False})

    sleep(30)

    # kill all the runing riaps actors
    for target in runtime.get_active_config("targets"):
        deployerId = "killer_" + target["host"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})

    # Stop discovery
    for target in runtime.get_active_config("targets"):
        deployerId = "discostop_" + target["host"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})
    sleep(10)



'''
def test_reach_discovery():
    for target in runtime.get_active_config("targets"):
        deployerId = "disco" + target["actor"]
        deployer = runtime.get_deployer(deployerId)
        deployer.start(deployerId, configs={"sync": True})

def test_pub_send():
    for target in runtime.get_active_config("targets"):
        deployer = runtime.get_deployer(target["actor"])
        deployer.start(target["actor"], configs={"sync": False})

    sleep(20)

def validate_pub_send():
    print("Validate")

    pubActorName = "ActorTest1p"
    subActorName = "ActorTest1s"
    appName = "test_1_1"

    # Check the configuration, please adjust the names according to the config.json and components log (if necessary)
    # We make sure, that we collect the right logs
    assert runtime.get_active_config("targets")[0]["actor"] == pubActorName, "Publisher actor name doesn't match"
    assert runtime.get_active_config("targets")[1]["actor"] == subActorName, "Subscriber actor name doesn't match"
    assert runtime.get_active_config("app_dir") == appName, "Application name doesn't match"

    pub_log_name = "{0}-{1}_{2}.log".format(pubActorName, appName,pubActorName)
    pub_log_file = os.path.join(perf.LOGS_DIRECTORY, pub_log_name)
    pub_logs = testutilities.get_log_for_test("test_pub_send", pub_log_file, "12:00:00")
    assert "Sent messages: 1" in pub_logs, "Publisher couldn't send any messages"
    assert "Sent messages: 5" in pub_logs, "Publisher couldn't send 5 messages"

    sub_log_name = "{0}-{1}_{2}.log".format(subActorName, appName, subActorName)
    sub_log_file = os.path.join(perf.LOGS_DIRECTORY, sub_log_name)
    sub_logs = testutilities.get_log_for_test("test_pub_send", sub_log_file, "12:00:00")

    assert "Received messages: 1" in sub_logs, "Subscriber didn't get any messages"
    assert "Received messages: 5" in sub_logs, "Subscriber didn't get 5 messages"
'''