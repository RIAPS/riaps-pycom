################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
Modbus/port/hal_sci.obj: ../Modbus/port/hal_sci.c $(GEN_OPTS) $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C2000 Compiler'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/cl2000" -v28 -ml -mt --cla_support=cla1 --float_support=fpu32 --tmu_support=tmu0 --vcu_support=vcu2 --include_path="C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/include" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/port" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/rtu" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_headers/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_common/include" --advice:performance=all -g --define=CPU1 --diag_warning=225 --display_error_number --diag_suppress=10063 --preproc_with_compile --preproc_dependency="Modbus/port/hal_sci.pp" --obj_directory="Modbus/port" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

Modbus/port/portevent.obj: ../Modbus/port/portevent.c $(GEN_OPTS) $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C2000 Compiler'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/cl2000" -v28 -ml -mt --cla_support=cla1 --float_support=fpu32 --tmu_support=tmu0 --vcu_support=vcu2 --include_path="C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/include" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/port" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/rtu" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_headers/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_common/include" --advice:performance=all -g --define=CPU1 --diag_warning=225 --display_error_number --diag_suppress=10063 --preproc_with_compile --preproc_dependency="Modbus/port/portevent.pp" --obj_directory="Modbus/port" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

Modbus/port/portserial.obj: ../Modbus/port/portserial.c $(GEN_OPTS) $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C2000 Compiler'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/cl2000" -v28 -ml -mt --cla_support=cla1 --float_support=fpu32 --tmu_support=tmu0 --vcu_support=vcu2 --include_path="C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/include" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/port" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/rtu" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_headers/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_common/include" --advice:performance=all -g --define=CPU1 --diag_warning=225 --display_error_number --diag_suppress=10063 --preproc_with_compile --preproc_dependency="Modbus/port/portserial.pp" --obj_directory="Modbus/port" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

Modbus/port/porttimer.obj: ../Modbus/port/porttimer.c $(GEN_OPTS) $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C2000 Compiler'
	"C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/bin/cl2000" -v28 -ml -mt --cla_support=cla1 --float_support=fpu32 --tmu_support=tmu0 --vcu_support=vcu2 --include_path="C:/ti/ccsv6/tools/compiler/ti-cgt-c2000_6.4.12/include" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/port" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/rtu" --include_path="C:/Users/htu/CCS_Project/F28377_MODBUS/Modbus/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_headers/include" --include_path="C:/ti/controlSUITE/device_support/F2837xS/v200/F2837xS_common/include" --advice:performance=all -g --define=CPU1 --diag_warning=225 --display_error_number --diag_suppress=10063 --preproc_with_compile --preproc_dependency="Modbus/port/porttimer.pp" --obj_directory="Modbus/port" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


