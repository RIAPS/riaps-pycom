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
'''
def validate_pub_send_pub_first():
    print("Validate, pubsub 1:1 pub first")

    subActorName = "ActorTestN1s_loc"

    testcase = "pubfirst_" + subActorName

    sub_log_name = "{0}-{1}_{2}.log".format(testcase, "pubfirst", subActorName)
    sub_log_file = os.path.join(perf.LOGS_DIRECTORY, sub_log_name)
    sub_logs = testutilities.get_log_for_test("test_pub_send_pub_first", sub_log_file, "12:00:00")
    assert "Received messages: 10" in sub_logs>2, "Subscriber didn't get enough messages"

    for target in runtime.get_active_config("targets"):
        if target["actor"] != subActorName:
            pubActorName = target["actor"]
            testcase = "pubfirst_" + pubActorName
            pub_log_name = "{0}-{1}.log".format(testcase, testcase)
            pub_log_file = os.path.join(perf.LOGS_DIRECTORY, pub_log_name)
            pub_logs = testutilities.get_log_for_test("test_pub_send_pub_first", pub_log_file, "12:00:00")

            assert "Sent messages: 5" in pub_logs, "Publisher (" + pubActorName +") couldn't send enough messages"
'''
