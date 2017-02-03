import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep

def test_pub_sub():

    print("Start test: pub_sub N:N local")



    for target in runtime.get_active_config("targets"):
        testId = target["actor"]
        print("Start testcase: {0}".format(testId))
        deployer = runtime.get_deployer(testId)
        deployer.start(testId, configs={"sync": False,
                                'args': [runtime.get_active_config('app_dir'),
                                         runtime.get_active_config('app_dir') + '.json',
                                         testId,
                                         '--logfile="' + testId + '.log"']})


    sleep(40)
    
def validate_pub_sub():
    print("Validate, pubsub N:N")

    # ActorA, CompA
    log_name = "ActorTestNN_A-CompA_ActorTestNN_A.log"
    log_path = os.path.join(perf.LOGS_DIRECTORY, log_name)
    logs = testutilities.get_log_for_test("test_pub_sub", log_path, "12:00:00")
    assert "Sent messages: topic1_10" in logs, "CompA in ActorA couldn't send enough topic1 messages"
    assert "Sent messages: topic2_10" in logs, "CompA in ActorA couldn't send enough topic2 messages"


    # ActorA, CompB
    log_name = "ActorTestNN_A-CompB_ActorTestNN_A.log"
    log_path = os.path.join(perf.LOGS_DIRECTORY, log_name)
    logs = testutilities.get_log_for_test("test_pub_sub", log_path, "12:00:00")
    assert "Received message: topic2_15" in logs, "CompB in ActorA couldn't get enough topic2 messages"
    assert "Received message: topic3_15" in logs, "CompB in ActorA couldn't get enough topic3 messages"

    # ActorB, CompC
    log_name = "ActorTestNN_B-CompC_ActorTestNN_B.log"
    log_path = os.path.join(perf.LOGS_DIRECTORY, log_name)
    logs = testutilities.get_log_for_test("test_pub_sub", log_path, "12:00:00")
    assert "Sent message: topic3_10" in logs, "CompC in ActorB couldn't send enough topic3 messages"
    assert "Received message: topic1_13" in logs, "CompC in ActorB couldn't get enough topic1 messages"

    # ActorC, CompB
    log_name = "ActorTestNN_C-CompB_ActorTestNN_C.log"
    log_path = os.path.join(perf.LOGS_DIRECTORY, log_name)
    logs = testutilities.get_log_for_test("test_pub_sub", log_path, "12:00:00")
    assert "Received message: topic2_15" in logs, "CompB in ActorC couldn't get enough topic2 messages"
    assert "Received message: topic3_15" in logs, "CompB in ActorC couldn't get enough topic3 messages"
