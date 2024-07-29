from invoke import Context, task

@task
def assert_role_in(c: Context, *args):
    if c.config.role in args:
        return
    if c.config.role == "hostlist":
        return
    else:
        print(f"Cannot run this command for role \"{c.config.role}\"")
    exit(-1)

@task
def assert_role_not_in(c: Context, *args):
    if c.config.role in args:
        print(f"Cannot run this command for role \"{c.config.role}\"")
        exit(-1)
   
