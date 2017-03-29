/*
 * main.c
 */
/* ----------------------- DSP includes ----------------------------------*/
#include "F28x_Project.h"  // Device Headerfile and Examples Include File

/* ----------------------- Modbus includes --------------------------------*/
#include "mb.h"
#include "port.h"
#include "mbport.h"
#include "mbrtu.h"
#include "mb_interface.h"

void InitScibGpio();
/*
// These are defined by the linker (see F28335.cmd)
extern Uint16 RamfuncsLoadStart;
extern Uint16 RamfuncsLoadEnd;
extern Uint16 RamfuncsRunStart;
*/
/*-------------------------------------------------------------------------*/

float Pref;
int Active;


void main(void) {
	

	   InitSysCtrl();



	   InitCpuTimers(); //Initialize all CPU timers to known states

	   DINT;


	// Initialize PIE control registers to their default state.
	// The default state is all PIE interrupts disabled and flags
	// are cleared.
	// This function is found in the DSP2833x_PieCtrl.c file.
	   InitPieCtrl();

	// Disable CPU interrupts and clear all CPU interrupt flags:
	   IER = 0x0000;
	   IFR = 0x0000;

	// Initialize the PIE vector table with pointers to the shell Interrupt
	// Service Routines (ISR).
	// This will populate the entire table, even if the interrupt
	// is not used in this example.  This is useful for debug purposes.
	// The shell ISR routines are found in DSP2833x_DefaultIsr.c.
	// This function is found in DSP2833x_PieVect.c.
	   InitPieVectTable();

	// Interrupts that are used in this example are re-mapped to
	// ISR functions found within this file.
	  EALLOW;	// This is needed to write to EALLOW protected registers
	  PieVectTable.SCIB_TX_INT	= &SciTxIsrHandler;
	  PieVectTable.SCIB_RX_INT 	= &SciRxIsrHandler;
	  PieVectTable.TIMER0_INT 		= &CpuTimer0IsrHandler;
	  EDIS;   // This is needed to disable write to EALLOW protected registers

	// Copy time critical code and Flash setup code to RAM
	 // MemCopy(&RamfuncsLoadStart, &RamfuncsLoadEnd, &RamfuncsRunStart);

	  // Enable interrupts required for this example
	 PieCtrlRegs.PIECTRL.bit.ENPIE 	= 1;   // Enable the PIE block
	 PieCtrlRegs.PIEIER9.bit.INTx3	= 1;   // PIE Group 9, INT3 //SCIRXINTB_ISR
	 PieCtrlRegs.PIEIER9.bit.INTx4 	= 1;   // PIE Group 9, INT4 FOR SCIB TX
	 PieCtrlRegs.PIEIER1.bit.INTx7 	= 1;   // TINT0 in the PIE: Group 1 interrupt 7

	 IER 	|= M_INT9; //SCI Tx, Rx ISR
	 IER 	|= M_INT1; //CPU Timer ISR

	 EINT;

	 InitScibGpio(); //Configure pins GPIO 14 and 15 for SCIB

	 ModbusInit();

	 for (;;)
	 {
		 ModbusPoll();
	 }


}


void InitScibGpio()
{
	 EALLOW;

	       GpioCtrlRegs.GPAPUD.bit.GPIO14 = 0;	   // Enable pull-up for GPIO14 (SCITXDB)
	       GpioCtrlRegs.GPAPUD.bit.GPIO15 = 0;    // Enable pull-up for GPIO15 (SCIRXDB)
	       GpioCtrlRegs.GPAQSEL1.bit.GPIO15 = 3;  // Asynch input GPIO15 (SCIRXDB)
	       GpioCtrlRegs.GPAMUX1.bit.GPIO14 = 2;   // Configure GPIO14 for SCITXDB operation
	       GpioCtrlRegs.GPAMUX1.bit.GPIO15 = 2;   // Configure GPIO15 for SCIRXDB operation

	 EDIS;

}
