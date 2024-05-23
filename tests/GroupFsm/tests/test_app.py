import pathlib
import pytest
import time
from riaps.test_suite import test_api
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
