from invoke import Context, task

@task
def assert_role_in(c: Context, *args):
    if c.config.role in args:
        return
    if c.config.role == "hostlist":
        print(f"Cannot run this command for custom hostlists, specify a role")
    else:
        print(f"Cannot run this command for role \"{c.config.role}\"")
    exit(-1)
