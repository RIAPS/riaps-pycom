import json
import multiprocessing
import watchdog
import watchdog.events
import watchdog.observers
import os
import pytest
import queue
import time

from riaps.ctrl.ctrl import Controller
from riaps.utils.config import Config
import riaps.fabfile as fab
from fabric.api import execute
fab.env.use_ssh_config = True
required_clients = ['10.1.1.111',
                    '10.1.1.115',
                    '10.1.1.133',
                    '10.1.1.135',
                    '10.1.1.132',
                    '10.1.1.137',
                    '10.1.1.120',
                    '10.1.1.112',
                    '10.1.1.134',
                    '10.1.1.109',
                    '10.1.1.136',
                    '10.1.1.118',
                    '10.1.1.126',
                    '10.1.1.114',
                    '10.1.1.129',
                    '10.1.1.110',
                    '10.1.1.124',
                    '10.1.1.108',
                    '10.1.1.131',
                    '10.1.1.141',
                    '10.1.1.119',
                    '10.1.1.125',
                    '10.1.1.127',
                    '10.1.1.123',
                    '10.1.1.113',
                    '10.1.1.117',
                    '10.1.1.122',
                    '10.1.1.116',
                    '10.1.1.130',
                    '10.1.1.138',
                    '10.1.1.128',
                    '10.1.1.121',]


# @pytest.mark.skip
def test_sanity():
    assert True


class FileHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, event_q):
        self.event_q = event_q

    def on_any_event(self, event):
        pass
        # print(f"{event.event_type}, {event.src_path}")

    def on_modified(self, event):
        # print(f"on_modified: {event.src_path}")
        self.event_q.put(f"{event.src_path}")


def test_cli(c,clients):
    # event_q = multiprocessing.Queue
    # event_q = queue.Queue()
    # file_event_handler = FileHandler(event_q=event_q)
    # observer = watchdog.observers.Observer()
    # hardcoded_path = "/home/riaps/projects/RIAPS/riaps-pycom/src/scripts"
    # observer.schedule(file_event_handler, path=hardcoded_path, recursive=False)
    # observer.start()

    app_folder = "/home/riaps/riaps-pycom/tests/Group"
    # c.start()

    try:
        c.setAppFolder(app_folder)
        app_name = c.compileApplication("group.riaps", app_folder)
        depl_file = "group.depl"
        also_app_name = c.compileDeployment(depl_file)

        # start
        c.startRedis()
        c.discoType = 'redis'
        # c.startDht()
        c.startService()

        # wait for clients to be discovered
        known_clients = []
        counter = 300
        while not set(clients).issubset(set(known_clients)):
            known_clients = c.getClients()
            print(f"{len(known_clients)} known clients: {known_clients}")
            time.sleep(1)
            counter -= 1
            if counter <= 0:
                print("ERROR: wait for clients timed out")
                raise

        launch_time = fab.sys.local('date -u +"%Y-%m-%d %H:%M:%S"',capture=True).stdout


        # launch application
        print(f"{launch_time}: launch app")
        is_app_launched = c.launchByName(app_name)
        # downloadApp (line 512). Does the 'I' mean 'installed'?
        # launchByName (line 746)
        print(f"app launched? {is_app_launched}")

        # TODO: get events from the queue.
        #  Include a timeout perhaps?
        #  open file and read new lines when there
        #  has been a change, and do any testing.

        files = {}
        active_senders = []
        not_done = False

        while not_done:
            event_source = event_q.get()
            if ".log" in event_source:
                print(f"Event source: {event_source}")
                file_name = os.path.basename(event_source)
                if file_name not in files:
                    file = open(event_source, "r")
                    files[file_name] = {"file": file,
                                        "peers": [],
                                        "peers_known": False}

                file_data = files[file_name]

                for line in file_data["file"]:
                    print(f"file: {file_name}, line: {line}")
                    parts = line.split("::")
                    # print(f"file: {file_name}, last part: {parts[-2]}")

                    if "peer" in line:
                        name = line.split(" ")[1]
                        file_data["peers"].append(name)
                        # if active_senders in file_data["peers"]:
                        #     print(f"RECEIVE ALL ACTIVE: TRUE")
                        # else:
                        #     print(f"RECEIVE ALL ACTIVE: FALSE")

                    # TODO: at some point make check that peers matches up with required clients

                    if "uuid" in line:
                        msg = json.loads(parts[-2])
                        sender = msg["uuid"]
                        active_senders.append(sender)

                    if "known_senders" in line:
                        try:
                            known_senders = json.loads(parts[-2])
                        except NameError as e:
                            print(f"Exception: {e}")
                        num_senders = len(known_senders["known_senders"])

                        if num_senders == 5:
                            file_data["peers_known"] = True

                            for f in files:
                                if files[f]["peers_known"]:
                                    done = True
                                else:
                                    break

        # print(f"All nodes have all subscriptions active")

        manual_run = False
        if manual_run:
            done = input("Provide input when ready to stop")
        else:
            for i in range(60):
                if i%5 == 0:
                    print(f"App is running: {i}")
                time.sleep(1)

        # Halt application
        print("Halt app")
        is_app_halted = c.haltByName(app_name)
        # haltByName (line 799).
        print(f"app halted? {is_app_halted}")

        time.sleep(2)

        # _ = input("Paused for log collection. Press any key when ready...")
        # jrnlstr = rf'journalctl -u riaps-deplo.service --output=cat --since \"{launch_time}\" > /home/riaps/riaps_apps/{app_name}/journal.log'
        jrnlstr = rf'journalctl -o cat -u riaps-deplo.service --since \"{launch_time}\" > /home/riaps/riaps_apps/{app_name}/journal.log'
        cmdstr = f"""riaps_fab -i ~/.ssh/id_rsa.key -H {",".join(clients)} sys.sudo:'"{jrnlstr}"'"""
        res = fab.sys.local(cmdstr,capture=True)


        getAppLogscmdStr = "riaps_fab -i ~/.ssh/id_rsa.key -H %s riaps.getAppLogs:%s" % (",".join(clients),app_name)
        res = fab.sys.local(getAppLogscmdStr,capture=True)




    finally:
        # Remove application
        print("remove app")
        c.removeAppByName(app_name)  # has no return value.
        # removeAppByName (line 914).
        print("app removed")

        # Stop controller
        print("Stop controller")
        c.stop()
        print("controller stopped")

    # observer.stop()

def make_depl(clientList):
    path = '/home/riaps/riaps-pycom/tests/Group/group.depl'

    if os.path.isfile(path):
        os.remove(path)

    with open(path,'w') as fd:
        fd.write("app GroupFSM {\n")
        for c in clientList:
            fd.write(f"    on ({c}) StateGroupie();\n")
        fd.write("}\n")


def ipv4_to_hostname(ip: str) -> str:
    name = fab.sys.local(f"avahi-resolve-address {ip}",capture=True).stdout.split()[-1]
    # assert(name.find('riaps-') > 0, f"Bad name lookup: {s} -> {name}")
    return name

if __name__ == "__main__":
    fab_logfile_src = os.path.join(os.getcwd(),'tests','Group','logs')
    fab_logfile_dest = os.path.join(os.getcwd(),'logs')

    the_config = Config()
    the_controller = Controller(port=8888, script="-")
    for num in [2,3,4,5,7,10,15,20,32]:
        clientlist = required_clients[0:num]
        make_depl(clientlist)
        test_cli(the_controller, clientlist)
        time.sleep(3)
        for node_dir in os.scandir(fab_logfile_src):
            if os.path.isfile(node_dir): continue
            hostname = ipv4_to_hostname(node_dir.name)
            cmdstr = f'''mv {fab_logfile_src}/{node_dir.name} {fab_logfile_src}/{hostname}'''
            _ = fab.sys.local(cmdstr,capture=True)
        cmdstr = f'''mv -v {fab_logfile_src} {fab_logfile_dest}-{num}'''
        res = fab.sys.local(cmdstr)
        # print(f"mv result: {res.stdout, res.stderr}")
        if(num < 10):
            time.sleep(10)
    

    # hosts = set(['riaps-2839.local','riaps-164c.local','riaps-e835.local','riaps-ef9f.local',
    #          'riaps-d521.local','riaps-cdee.local','riaps-1180.local','riaps-e22d.local',
    #          'riaps-feb5.local','riaps-4797.local','riaps-eb18.local','riaps-fea3.local',
    #          'riaps-a0a6.local','riaps-923a.local','riaps-be53.local','riaps-da04.local',
    #          'riaps-f913.local','riaps-1d35.local','riaps-e528.local','riaps-93bb.local',
    #          'riaps-e7b8.local','riaps-23c6.local','riaps-f365.local','riaps-8be2.local',
    #          'riaps-e7b9.local','riaps-da61.local','riaps-20fb.local','riaps-4930.local',
    #          'riaps-7030.local','riaps-5df2.local','riaps-1610.local','riaps-da2e.local'])

    # nodes = ['10.1.1.130', '10.1.1.114', '10.1.1.116', '10.1.1.127', '10.1.1.109', '10.1.1.134', '10.1.1.113', '10.1.1.131', '10.1.1.141', '10.1.1.133', '10.1.1.123', '10.1.1.129', '10.1.1.120', '10.1.1.126', '10.1.1.137', '10.1.1.132', '10.1.1.122', '10.1.1.121', '10.1.1.112', '10.1.1.125', '10.1.1.110', '10.1.1.108', '10.1.1.136', '10.1.1.128', '10.1.1.124', '10.1.1.115', '10.1.1.118', '10.1.1.117', '10.1.1.119', '10.1.1.135', '10.1.1.111']
    # for n in nodes:
    #     name = fab.sys.local(f"avahi-resolve-address {n}",capture=True).stdout.split()[-1]
    #     hosts.remove(name)
    # print(hosts)
    

