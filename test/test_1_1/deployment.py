import os

import zopkio.adhoc_deployer as adhoc_deployer
import zopkio.runtime as runtime


def setup_suite():
    runtime.set_user("ubuntu", "temppwd")

    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              runtime.get_active_config('app_dir'),
                              runtime.get_active_config('model_file'))

    for target in runtime.get_active_config('targets'):
        model_deployer = adhoc_deployer.SSHDeployer(target["actor"], {
            'executable': model_path,
            'install_path': os.path.join(runtime.get_active_config('riaps_apps_path'),
                                         runtime.get_active_config('app_dir')),
            'hostname': target["host"],
            'start_command': "/home/ubuntu/.local/bin/riaps_actor",
            'args': [runtime.get_active_config('app_dir'),
                     runtime.get_active_config('app_dir') + '.json',
                     target["actor"]],
            'env': {"PATH": "$PATH:/home/ubuntu/.local/bin/",
                    "RIAPSHOME": "/home/ubuntu/.local/riaps",
                    "RIAPSAPPS": "/home/ubuntu/riaps_apps"},
            'terminate_only': True,
            'pid_keyword': model_path,
            'post_install_cmds': ["/home/ubuntu/.local/bin/riaps_lang " + runtime.get_active_config('model_file')]
        })
        runtime.set_deployer(target["actor"], model_deployer)
        model_deployer.install(target["actor"])

        for component in runtime.get_active_config('components_py'):
            localPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     runtime.get_active_config('app_dir'),
                                     component)
            targetPath = os.path.join(runtime.get_active_config('riaps_apps_path'), runtime.get_active_config('app_dir'))
            component_deployer = adhoc_deployer.SSHDeployer(component, {
                'executable': localPath,
                'install_path': targetPath,
                'hostname': target["host"],
                'start_command': "/home/ubuntu/.local/bin/riaps_actor",
                'args': [runtime.get_active_config('app_dir'),
                         runtime.get_active_config('app_dir') + '.json',
                         target["actor"]],
                'env': {"PATH": "$PATH:/home/ubuntu/.local/bin/",
                        "RIAPSHOME": "/home/ubuntu/.local/riaps",
                        "RIAPSAPPS": "/home/ubuntu/riaps_apps"},
                'terminate_only': True,
                'pid_keyword': component,
            })
            runtime.set_deployer(component, component_deployer)
            component_deployer.install(component)

    print("Deployment done.")


    # for host in runtime.get_active_config('target_hosts'):
    #     global model_deployer
    #     model_deployer = adhoc_deployer.SSHDeployer("modelDeployer", {
    #         'executable': model_path,
    #         'install_path':  os.path.join(runtime.get_active_config('riaps_apps_path'),
    #                                       runtime.get_active_config('app_dir')),
    #         'hostname': host,
    #         'start_command': "/home/ubuntu/.local/bin/riaps_actor",
    #         'args': [runtime.get_active_config('app_dir'),
    #                      runtime.get_active_config('app_dir') + '.json',
    #                      runtime.get_active_config('actor_name')],
    #         'env': {"PATH": "$PATH:/home/ubuntu/.local/bin/",
    #                 "RIAPSHOME": "/home/ubuntu/.local/riaps",
    #                 "RIAPSAPPS": "/home/ubuntu/riaps_apps"},
    #         'terminate_only': True,
    #         'pid_keyword': model_path,
    #         'post_install_cmds': ["/home/ubuntu/.local/bin/riaps_lang " + runtime.get_active_config('model_file')]
    #     })
    #     runtime.set_deployer("modelDeployer", model_deployer)
    #     model_deployer.install("modelDeployer")


    # for host in runtime.get_active_config('target_hosts'):
    #     for component in runtime.get_active_config('components_py'):
    #         localPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                                  runtime.get_active_config('app_dir'),
    #                                  component)
    #         targetPath = os.path.join(runtime.get_active_config('riaps_apps_path'),runtime.get_active_config('app_dir'))
    #         component_deployer = adhoc_deployer.SSHDeployer(component, {
    #             'executable'   : localPath,
    #             'install_path' : targetPath,
    #             'hostname'     : host,
    #             'start_command': "/home/ubuntu/.local/bin/riaps_actor",
    #             'args': [runtime.get_active_config('app_dir'),
    #                      runtime.get_active_config('app_dir') + '.json',
    #                      runtime.get_active_config('actor_name')],
    #             'env': {"PATH": "$PATH:/home/ubuntu/.local/bin/",
    #                     "RIAPSHOME": "/home/ubuntu/.local/riaps",
    #                     "RIAPSAPPS": "/home/ubuntu/riaps_apps"},
    #             'terminate_only': True,
    #             'pid_keyword': component,
    #         })
    #         runtime.set_deployer(component, component_deployer)
    #         component_deployer.install(component)



def setup():
    print("Setup")
    # for process in server_deployer.get_processes():
    #  server_deployer.start(process.unique_id)


def teardown():
    print("Teardown")
    # for process in client_deployer.get_processes():
    #  client_deployer.stop(process.unique_id)


def teardown_suite():
    print("Teardown suite")
    #for process in model_deployer.get_processes():
    #    model_deployer.undeploy(process.unique_id)
