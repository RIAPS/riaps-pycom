import pathlib
import pytest
import queue
import time
from riaps.test_suite import test_api, monitor
from riaps.test_suite.fixtures import utils

# ------------ #
# -- Config -- #
# ------------ #
scott_config = {
    "VM_IP": "192.168.0.100",
    "app_folder_path": pathlib.Path(__file__).parents[1],
    "app_file_name": "group.riaps",
    "depl_file_name": "group.depl",
}


configs = {"scott": scott_config}

test_cfg = configs["scott"]


# ------------------ #
# -- Config tests -- #
# ------------------ #
def test_clients():
    app_folder_path = test_cfg["app_folder_path"]
    depl_file_name = test_cfg["depl_file_name"]
    log_config_path = f"{app_folder_path}/riaps-log.conf"
    client_list = utils.get_client_list(file_path=f"{app_folder_path}/{depl_file_name}")
    print(f"client list: {client_list}")


# -------------- #
# -- App test -- #
# -------------- #
@pytest.mark.parametrize(
    "platform_log_server", [{"server_ip": test_cfg["VM_IP"]}], indirect=True
)
@pytest.mark.parametrize(
    "log_server",
    indirect=True,
    argvalues=[
        {
            "server_ip": test_cfg["VM_IP"],
            "log_config_path": f"{test_cfg['app_folder_path']}/riaps-log.conf",
        }
    ],
)
def test_app(platform_log_server, log_server):

    app_folder_path = test_cfg["app_folder_path"]
    app_file_name = test_cfg["app_file_name"]
    depl_file_name = test_cfg["depl_file_name"]

    client_list = utils.get_client_list(file_path=f"{app_folder_path}/{depl_file_name}")
    print(f"client list: {client_list}")

    controller, app_name = test_api.launch_riaps_app(
        app_folder_path=app_folder_path,
        app_file_name=app_file_name,
        depl_file_name=depl_file_name,
        database_type="dht",
        required_clients=client_list,
    )

    input("Press a key to terminate the app\n")
    test_api.terminate_riaps_app(controller, app_name)
    print(f"Test complete at {time.time()}")


# -------------- #
# -- Watch App -- #
# -------------- #


@pytest.mark.parametrize(
    "platform_log_server", [{"server_ip": test_cfg["VM_IP"]}], indirect=True
)
@pytest.mark.parametrize(
    "log_server",
    indirect=True,
    argvalues=[
        {
            "server_ip": test_cfg["VM_IP"],
            "log_config_path": f"{test_cfg['app_folder_path']}/riaps-log.conf",
        }
    ],
)
def test_watch_app(platform_log_server, log_server, testslogger):

    event_q = queue.Queue()
    task_q = queue.Queue()
    end_time = time.time() + 30

    event_q_monitor_thread = monitor.EventQMonitorThread(
        event_q, task_q, end_time=end_time, handler=my_watcher
    )
    event_q_monitor_thread.start()

    test_app(platform_log_server, log_server)


def my_watcher(event_q, task_q, end_time):
    files = {}
    while end_time > time.time():
        try:
            event_source = event_q.get(10)  #
        except queue.Empty:
            print(f"File event queue is empty")
            continue

        if ".log" not in event_source:  # required to filter out the directory events
            continue

        file_name = pathlib.Path(event_source).name
        file_data = files.get(file_name, None)
        if file_data is None:
            file_handle = open(event_source, "r")
            files[file_name] = {"fh": file_handle, "offset": 0}
        else:
            file_handle = file_data["fh"]

        # if not any(node_id in file_name for node_id in test_cfg["node_ids"]):
        #     continue  # Not interested in this file

        for line in file_handle:
            files[file_name]["offset"] += len(line)

            if "FOLLOWER" in line:
                print(f"file: {file_name} line: {line}")
