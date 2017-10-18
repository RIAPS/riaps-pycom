import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep


def test_req_rep():
    for target in runtime.get_active_config("targets"):
        actorName = target["actor"]
        deployer = runtime.get_deployer(actorName)
        deployer.start(target["actor"], configs={"sync": False,
                                            'args': [runtime.get_active_config('app_dir'),
                                             runtime.get_active_config('app_dir') + '.json',
                                             actorName,
                                             '--logfile="' + actorName + '.log"']})
        sleep(2)

    sleep(30)


def validate_req_rep():
    actorRep = "Actor11_B_loc_async"
    actorReq = "Actor11_A_loc_async"

    rep_log_name = "{0}-{1}.log".format(actorRep, actorRep)
    rep_log_file = os.path.join(perf.LOGS_DIRECTORY, rep_log_name)
    rep_logs = testutilities.get_log_for_test("test_req_rep", rep_log_file, "12:00:00")

    assert "Got request: 40" in rep_logs, "Response port didn't get enough requests"
    assert "Sent response: 40" in rep_logs, "Response port couldn't send enough messageges"

    rep_log_name = "{0}-{1}.log".format(actorReq, actorReq)
    rep_log_file = os.path.join(perf.LOGS_DIRECTORY, rep_log_name)
    rep_logs = testutilities.get_log_for_test("test_req_rep", rep_log_file, "12:00:00")

    assert "Sent request: 40" in rep_logs, "Request port didn't send enough requests"
    assert "Got response: 40" in rep_logs, "Response port didn't get enough messageges"
