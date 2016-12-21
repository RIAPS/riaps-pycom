import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep

def test_pub_send():
  model_deployer = runtime.get_deployer("modelDeployer")
  model_deployer.start("modelDeployer", configs={"sync": False})
  sleep(20)

def validate_pub_send():
  pub_log_file = os.path.join(perf.LOGS_DIRECTORY, "modelDeployer-test_N_N.log")
  pub_logs = testutilities.get_log_for_test("test_pub_send", pub_log_file, "12:00:00")
  assert "Sent messages: 1" in pub_logs > 2, "Publisher was unable to send messages"
  assert "Sent messages: 5" in pub_logs > 2, "Publisher couldn't send at least 5 messages"
  assert "Received messages: 5" in pub_logs >2, "Subscriber didn't get any messages"