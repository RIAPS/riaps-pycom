import os
import zopkio.runtime as runtime

LOGS_DIRECTORY = "/tmp/riaps_test/collected_logs/testPubSub/test_N_N/"
OUTPUT_DIRECTORY = "/tmp/riaps_test/results/"

def machine_logs():
  results = {}

  for target in runtime.get_active_config("targets"):
    testcase = target["actor"]

    if testcase=="ActorTestNN_A":
      logPathCompA = "/tmp/CompA_{0}.log".format(testcase)
      logPathCompB = "/tmp/CompB_{0}.log".format(testcase)
      results[testcase] = [logPathCompA, logPathCompB]
    elif testcase=="ActorTestNN_B":
      logPathCompC = "/tmp/CompC_{0}.log".format(testcase)
      results[testcase] = [logPathCompC]
    elif testcase=="ActorTestNN_C":
      logPathCompB = "/tmp/CompB_{0}.log".format(testcase)
      results[testcase] = [logPathCompB]


  return results

def naarad_logs():
  return {

  }


def naarad_config():
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), "naarad.cfg")
