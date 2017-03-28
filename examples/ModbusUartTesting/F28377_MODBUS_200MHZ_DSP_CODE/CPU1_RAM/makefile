################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

CG_TOOL_ROOT := C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12

GEN_OPTS__FLAG := 
GEN_CMDS__FLAG := 

ORDERED_OBJS += \
"./F2837xS_CodeStartBranch.obj" \
"./F2837xS_CpuTimers.obj" \
"./F2837xS_DefaultISR.obj" \
"./F2837xS_GlobalVariableDefs.obj" \
"./F2837xS_Gpio.obj" \
"./F2837xS_PieCtrl.obj" \
"./F2837xS_PieVect.obj" \
"./F2837xS_SysCtrl.obj" \
"./F2837xS_usDelay.obj" \
"./main.obj" \
"./Modbus/rtu/mbcrc.obj" \
"./Modbus/rtu/mbrtu.obj" \
"./Modbus/port/hal_sci.obj" \
"./Modbus/port/portevent.obj" \
"./Modbus/port/portserial.obj" \
"./Modbus/port/porttimer.obj" \
"./Modbus/mb.obj" \
"./Modbus/mb_interface.obj" \
"./Modbus/functions/mbfunccoils.obj" \
"./Modbus/functions/mbfuncdiag.obj" \
"./Modbus/functions/mbfuncdisc.obj" \
"./Modbus/functions/mbfuncholding.obj" \
"./Modbus/functions/mbfuncinput.obj" \
"./Modbus/functions/mbfuncother.obj" \
"./Modbus/functions/mbutils.obj" \
"../cmd/2837xS_Generic_RAM_lnk_tu.cmd" \
"../cmd/F2837xS_Headers_nonBIOS_tu.cmd" \
$(GEN_CMDS__FLAG) \
-l"rts2800_fpu32.lib" \
-l"libc.a" \

-include ../makefile.init

RM := DEL /F
RMDIR := RMDIR /S/Q

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir_vars.mk
-include cmd/subdir_vars.mk
-include Modbus/rtu/subdir_vars.mk
-include Modbus/port/subdir_vars.mk
-include Modbus/subdir_vars.mk
-include Modbus/functions/subdir_vars.mk
-include subdir_rules.mk
-include cmd/subdir_rules.mk
-include Modbus/rtu/subdir_rules.mk
-include Modbus/port/subdir_rules.mk
-include Modbus/subdir_rules.mk
-include Modbus/functions/subdir_rules.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(S62_DEPS)),)
-include $(S62_DEPS)
endif
ifneq ($(strip $(C64_DEPS)),)
-include $(C64_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(S55_DEPS)),)
-include $(S55_DEPS)
endif
ifneq ($(strip $(C67_DEPS)),)
-include $(C67_DEPS)
endif
ifneq ($(strip $(CLA_DEPS)),)
-include $(CLA_DEPS)
endif
ifneq ($(strip $(C??_DEPS)),)
-include $(C??_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(S??_DEPS)),)
-include $(S??_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(C62_DEPS)),)
-include $(C62_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(ASM_UPPER_DEPS)),)
-include $(ASM_UPPER_DEPS)
endif
ifneq ($(strip $(K_DEPS)),)
-include $(K_DEPS)
endif
ifneq ($(strip $(C43_DEPS)),)
-include $(C43_DEPS)
endif
ifneq ($(strip $(INO_DEPS)),)
-include $(INO_DEPS)
endif
ifneq ($(strip $(S67_DEPS)),)
-include $(S67_DEPS)
endif
ifneq ($(strip $(SA_DEPS)),)
-include $(SA_DEPS)
endif
ifneq ($(strip $(S43_DEPS)),)
-include $(S43_DEPS)
endif
ifneq ($(strip $(OPT_DEPS)),)
-include $(OPT_DEPS)
endif
ifneq ($(strip $(PDE_DEPS)),)
-include $(PDE_DEPS)
endif
ifneq ($(strip $(S64_DEPS)),)
-include $(S64_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(C55_DEPS)),)
-include $(C55_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXE_OUTPUTS += \
F28377_MODBUS_200MHZ.out \

EXE_OUTPUTS__QUOTED += \
"F28377_MODBUS_200MHZ.out" \

BIN_OUTPUTS += \
F28377_MODBUS_200MHZ.hex \

BIN_OUTPUTS__QUOTED += \
"F28377_MODBUS_200MHZ.hex" \


# All Target
all: F28377_MODBUS_200MHZ.out

# Tool invocations
F28377_MODBUS_200MHZ.out: $(OBJS) $(CMD_SRCS) $(GEN_CMDS)
	@echo 'Building target: $@'
	@echo 'Invoking: C2000 Linker'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/cl2000" -v28 -ml -mt --cla_support=cla1 --float_support=fpu32 --tmu_support=tmu0 --vcu_support=vcu2 --advice:performance=all -g --define=CPU1 --diag_warning=225 --display_error_number --diag_suppress=10063 -z -m"F28377_MODBUS_200MHZ.map" --stack_size=0x100 --warn_sections -i"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/lib" -i"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/include" --reread_libs --display_error_number --xml_link_info="F28377_MODBUS_200MHZ_linkInfo.xml" --entry_point=code_start --rom_model -o "F28377_MODBUS_200MHZ.out" $(ORDERED_OBJS)
	@echo 'Finished building target: $@'
	@echo ' '

F28377_MODBUS_200MHZ.hex: $(EXE_OUTPUTS)
	@echo 'Invoking: C2000 Hex Utility'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/hex2000"  -o "F28377_MODBUS_200MHZ.hex" $(EXE_OUTPUTS__QUOTED)
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(EXE_OUTPUTS__QUOTED)$(BIN_OUTPUTS__QUOTED)
	-$(RM) "F2837xS_CpuTimers.pp" "F2837xS_DefaultISR.pp" "F2837xS_GlobalVariableDefs.pp" "F2837xS_Gpio.pp" "F2837xS_PieCtrl.pp" "F2837xS_PieVect.pp" "F2837xS_SysCtrl.pp" "main.pp" "Modbus\rtu\mbcrc.pp" "Modbus\rtu\mbrtu.pp" "Modbus\port\hal_sci.pp" "Modbus\port\portevent.pp" "Modbus\port\portserial.pp" "Modbus\port\porttimer.pp" "Modbus\mb.pp" "Modbus\mb_interface.pp" "Modbus\functions\mbfunccoils.pp" "Modbus\functions\mbfuncdiag.pp" "Modbus\functions\mbfuncdisc.pp" "Modbus\functions\mbfuncholding.pp" "Modbus\functions\mbfuncinput.pp" "Modbus\functions\mbfuncother.pp" "Modbus\functions\mbutils.pp" 
	-$(RM) "F2837xS_CodeStartBranch.obj" "F2837xS_CpuTimers.obj" "F2837xS_DefaultISR.obj" "F2837xS_GlobalVariableDefs.obj" "F2837xS_Gpio.obj" "F2837xS_PieCtrl.obj" "F2837xS_PieVect.obj" "F2837xS_SysCtrl.obj" "F2837xS_usDelay.obj" "main.obj" "Modbus\rtu\mbcrc.obj" "Modbus\rtu\mbrtu.obj" "Modbus\port\hal_sci.obj" "Modbus\port\portevent.obj" "Modbus\port\portserial.obj" "Modbus\port\porttimer.obj" "Modbus\mb.obj" "Modbus\mb_interface.obj" "Modbus\functions\mbfunccoils.obj" "Modbus\functions\mbfuncdiag.obj" "Modbus\functions\mbfuncdisc.obj" "Modbus\functions\mbfuncholding.obj" "Modbus\functions\mbfuncinput.obj" "Modbus\functions\mbfuncother.obj" "Modbus\functions\mbutils.obj" 
	-$(RM) "F2837xS_CodeStartBranch.pp" "F2837xS_usDelay.pp" 
	-@echo 'Finished clean'
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets

