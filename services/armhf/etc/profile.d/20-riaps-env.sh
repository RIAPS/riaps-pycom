for i in `cat /etc/riaps/env.conf`;do export $i ;done
# RIAPS Device Slots
export SLOTS=/sys/devices/platform/bone_capemgr/slots
# RIAPS Device Pins
export PINS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pins

