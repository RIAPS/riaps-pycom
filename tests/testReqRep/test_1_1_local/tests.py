import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep


def test_req_rep():
    for target in runtime.get_active_config("targets"):
        deployer = runtime.get_deployer(target["actor"])
        deployer.start(target["actor"], configs={"sync": False})

    sleep(20)

'''
def validate_req_rep_send():
    print("Validate")

    repActorName = "ActorTest1rep"
    reqActorName = "ActorTest1req"
    appName = "test_1_1"

    # Check the configuration, please adjust the names according to the config.json and components log (if necessary)
    # We make sure, that we collect the right logs
    assert runtime.get_active_config("targets")[0]["actor"] == repActorName, "Response actor name doesn't match"
    assert runtime.get_active_config("targets")[1]["actor"] == reqActorName, "Request actor name doesn't match"
    assert runtime.get_active_config("app_dir") == appName, "Application name doesn't match"

    rep_log_name = "{0}-{1}_{2}.log".format(repActorName, appName,repActorName)
    rep_log_file = os.path.join(perf.LOGS_DIRECTORY, rep_log_name)
    rep_logs = testutilities.get_log_for_test("test_req_rep", rep_log_file, "12:00:00")
    assert "Got request: 1" in rep_logs, "Response port didn't get any requests"
    assert "Sent response: 1" in rep_logs, "Response port couldn't send any messageges"
    assert "Got request: 3" in rep_logs, "Response port didn't get at least 3 requests"
    assert "Sent response: 3" in rep_logs, "Response port couldn't send at least 3 messageges"

    req_log_name = "{0}-{1}_{2}.log".format(reqActorName, appName, reqActorName)
    req_log_file = os.path.join(perf.LOGS_DIRECTORY, req_log_name)
    req_logs = testutilities.get_log_for_test("test_req_rep", req_log_file, "12:00:00")

    assert "Sent request: 1" in req_logs, "Request port couldn't send any requests"
    assert "Got response: 1" in req_logs, "Request port didn't get any messageges"
    assert "Sent request: 3" in req_logs, "Request port couldn't send at least 3 requests"
    assert "Got response: 3" in req_logs, "Request port didn't get at least 3 messageges"

    #assert "Received messages: 1" in sub_logs, "Subscriber didn't get any messages"
    #assert "Received messages: 5" in sub_logs, "Subscriber didn't get 5 messages"
'''