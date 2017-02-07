import zopkio.runtime as runtime
import zopkio.test_utils as testutilities
import os
import perf
from time import sleep


def test_service_messaging():
    for target in runtime.get_active_config("targets"):
        deployer = runtime.get_deployer(target["host"])
        deployer.start(target["host"], configs={"sync": True})
        sleep(2)

    sleep(30)


def validate_service_messaging():
    for target in runtime.get_active_config("targets"):
        logname = target["host"]

        serv_log_name = "{0}-{1}.log".format(logname, logname)
        serv_log_file = os.path.join(perf.LOGS_DIRECTORY, serv_log_name)
        serv_logs = testutilities.get_log_for_test("test_service_messaging", serv_log_file, "12:00:00")

        assert "Disco response: ok" in serv_logs, "Response port didn't get enough requests"
        assert "Sent response: 40" in serv_logs, "Response port couldn't send enough messageges"

