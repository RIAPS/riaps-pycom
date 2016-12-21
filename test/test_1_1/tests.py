import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep

def test_pub_send():
    for target in runtime.get_active_config("targets"):
        deployer = runtime.get_deployer(target["actor"])
        deployer.start(target["actor"], configs={"sync": False})

    sleep(20)

  # model_deployer = runtime.get_deployer("modelDeployer")
  # model_deployer.start("modelDeployer", configs={"sync": False})
  # sleep(15)
  #model_deployer.stop("modelDeployer")

#def validate_pub_send():
#    print("Validate")
  # pub_log_file = os.path.join(perf.LOGS_DIRECTORY, "modelDeployer-test_1_1.log")
  # pub_logs = testutilities.get_log_for_test("test_pub_send", pub_log_file, "12:00:00")
  # assert "Sent messages: 5" in pub_logs, "Did not send messages in publisher"
  # assert "Received messages: 5" in pub_logs, "Did not get messages in subscriber"