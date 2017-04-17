
import os
import zopkio.runtime as runtime

LOGS_DIRECTORY = "/tmp/riaps_test/collected_logs/testService/testCapnpMessaging/"
OUTPUT_DIRECTORY = "/tmp/riaps_test/results/"

def machine_logs():

  results = {}

  for target in runtime.get_active_config("targets"):
    logpath = "/tmp/testCapnpMessaging_{0}.log".format(target["host"])
    results[target["host"]] = [logpath]

  return results
  # return {
  #   "modelDeployer": ["/tmp/test_1_1.log"]
  # }

def naarad_logs():
  return {

  }


def naarad_config():
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), "naarad.cfg")
