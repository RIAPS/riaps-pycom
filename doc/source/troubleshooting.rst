Troubleshooting
===============

This page covers installation and runtime issues that are not obvious from error messages alone.

.. contents:: On this page
   :local:
   :depth: 2


``ZMQError: Bad address`` on riaps_deplo startup
-------------------------------------------------

**Symptom**

``riaps_deplo`` crashes within milliseconds of starting. Multiple threads fail simultaneously with::

    zmq.error.ZMQError: Bad address

The affected threads are ``SpcMonitorThread`` (spcmon.py), ``NICMonitor``, ``FMMonitor``,
and ``DeploymentManager`` (fm.py, depm.py). Concurrently, ``riaps_ctrl`` may log::

    ? Query: AttributeError("'NoneType' object has no attribute 'value'")

**Root cause**

``riaps_deplo`` uses ``zmq.Context.shadow(Zsys.init().value)`` to share a single ZMQ context
between pyzmq and czmq/zyre. This requires both libraries to link against the **same in-process
instance** of libzmq.

pip wheels for pyzmq bundle a private copy of libzmq inside
``pyzmq.libs/libzmq-<hash>.so``. When a pip-installed pyzmq is present alongside the system
czmq (which links against ``/usr/lib/x86_64-linux-gnu/libzmq.so.5``), two separate libzmq
instances are loaded into the process. A context pointer created by one instance is invalid
in the other, causing every ``context.socket()`` call to fail with ``Bad address``.

The ``? Query: AttributeError`` in ``riaps_ctrl`` is a downstream consequence: the controller
queries the newly-connected deplo node, the node crashes before answering, and ``res.value``
fails because ``res`` is ``None``.

**Diagnosis**

Check which libzmq pyzmq is actually using::

    find /usr/local/lib/python3.10/dist-packages/zmq -name "*.so" | head -1 | xargs ldd | grep zmq

- **System libzmq** (correct): ``libzmq.so.5 => /usr/lib/x86_64-linux-gnu/libzmq.so.5``
- **Bundled libzmq** (broken): path contains ``pyzmq.libs/``

You can also run the smoke test that mirrors the pattern in ``riaps_deplo`` directly::

    python3 -c "
    from czmq import Zsys
    import zmq
    ctx = Zsys.init()
    zctx = zmq.Context.shadow(ctx.value)
    Zsys.handler_reset()
    s = zctx.socket(zmq.ROUTER)
    s.close()
    print('OK')
    "

If this raises ``ZMQError: Bad address``, the bundled libzmq is the cause.

**Fix**

Reinstall pyzmq from source so it compiles against the system libzmq::

    sudo pip3 install --force-reinstall --no-binary pyzmq "pyzmq>=25.1.2"

The ``--no-binary`` flag is what matters: it forces a source build rather than downloading a
pre-built wheel. After reinstalling, rerun the smoke test above to confirm.

.. note::
   Any subsequent ``pip install --upgrade pyzmq`` (without ``--no-binary``) will revert to a
   bundled-libzmq wheel and re-introduce the problem. Always include ``--no-binary pyzmq``
   when upgrading.


riaps_deplo fails to connect to riaps_ctrl
------------------------------------------

**Symptom**

``riaps_deplo`` logs repeated connection failures::

    Failed to connect via rpyc[<ip>:8888]: [Errno 111] Connection refused

**Root cause**

``riaps_deplo`` connects to ``riaps_ctrl`` immediately on startup. The controller must be
running and listening on port 8888 before deplo is started.

**Service startup order**

Start services in this order:

1. ``sudo riaps_ctrl`` — the controller. This also manages the discovery service internally.
2. ``sudo -E riaps_deplo`` — the deployment manager.

Do **not** start ``riaps_disco`` manually. ``riaps_ctrl`` manages it.

Confirm ``riaps_ctrl`` is listening before starting deplo::

    ss -tlnp | grep 8888

The RPyC registry service must also be running (it is enabled at boot via systemd)::

    systemctl is-active riaps-rpyc-registry.service


NIC not found or ``Bad address`` on socket bind
------------------------------------------------

**Symptom**

``riaps_deplo`` warns that the configured network interface was not found, or zyre/czmq
fails to bind sockets.

**Cause**

The ``nic_name`` in ``/etc/riaps/riaps.conf`` names an interface that does not exist or has
no IPv4 address. ``riaps_deplo`` falls back to the first available interface, which may not
be the intended one.

**Fix**

Check which interfaces are available::

    ip addr show

Update ``nic_name`` in ``/etc/riaps/riaps.conf`` to match an interface that is up and has an
IPv4 address. For Tailscale-based setups, ``tailscale0`` is the correct value once the
Tailscale daemon is running.
