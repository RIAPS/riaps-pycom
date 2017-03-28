#include "hal_sci.h"

#define LSPCLK 	50000000

void  SciRxSet (volatile struct SCI_REGS* sci_regs_ptr, _Bool value)
{
    if (value == ENABLED)
    {
        (*sci_regs_ptr).SCICTL1.bit.RXENA = 1;
    }
    else
    {
        (*sci_regs_ptr).SCICTL1.bit.RXENA = 0;
    }
}

void  SciTxSet (volatile struct SCI_REGS* sci_regs_ptr, _Bool value)
{
    if (value == ENABLED)
    {
        (*sci_regs_ptr).SCICTL1.bit.TXENA = 1;
    }
    else
    {
        (*sci_regs_ptr).SCICTL1.bit.TXENA = 0;
    }    
}

void  SciRxIsrSet(volatile struct SCI_REGS* sci_regs_ptr, _Bool value)
{
    if (value == ENABLED)
    {
        (*sci_regs_ptr).SCICTL2.bit.RXBKINTENA = 1;
    }
    else
    {
        (*sci_regs_ptr).SCICTL2.bit.RXBKINTENA = 0;
    }
}

void  SciTxIsrSet(volatile struct SCI_REGS* sci_regs_ptr, _Bool value)
{
    if (value == ENABLED)
    {
        (*sci_regs_ptr).SCICTL2.bit.TXINTENA = 1;
    }
    else
    {
        (*sci_regs_ptr).SCICTL2.bit.TXINTENA = 0;
    }  
}

void SciTxIsrConfig (void)
{
    EALLOW;
	//--> SCI transmit interrupt handler function address mapping
	PieVectTable.SCIB_TX_INT	= &SciTxIsrHandler;
    //PieVectTable.SCITXINTA	= &SciTxIsrHandler; /* Uncomment for SCITXINTA*/
	EDIS;
	// SCI transmit isr
	IER 	|= M_INT9;
	// PIE Group 9, INT2 FOR SCIB TX
    PieCtrlRegs.PIEIER9.bit.INTx4 	= 1;
	//PieCtrlRegs.PIEIER9.bit.INTx2 	= 1; /* Uncomment for SCITXINTA*/
}


void SciRxIsrConfig (void)
{
	EALLOW;
	//--> SCI receive interrupt handler function address mapping
	PieVectTable.SCIB_RX_INT = &SciRxIsrHandler;
    //PieVectTable.SCITXINTA	= &SciTxIsrHandler; /* Uncomment for SCITXINTA*/
	EDIS;
	// SCI receive isr
	IER 	|= M_INT9;
	// PIE Group 9, INT2 FOR SCIB RX
    PieCtrlRegs.PIEIER9.bit.INTx3 	= 1;
	//PieCtrlRegs.PIEIER9.bit.INTx1 	= 1;/* Uncomment for SCITXINTA*/
}


void SciInit(volatile struct SCI_REGS* sci_regs_ptr, Uint32 baudrate)
{
    Uint32 baud_bits = 0;
    (*sci_regs_ptr).SCICCR.all = 0x0007;   // 1 stop bit,  No loopback
                                          // No parity,8 char bits,
                                          // async mode, idle-line protocol
	(*sci_regs_ptr).SCICTL1.all =0x0003;  // Enable TX, RX
                                          // Disable RX ERR, SLEEP, TXWAKE
	(*sci_regs_ptr).SCICTL2.all =0x0000;  // Tx/Rx interrupts Disabled

    baud_bits = (Uint32) (LSPCLK / (baudrate*8) - 1);

	// Configure the High and Low baud rate registers
	(*sci_regs_ptr).SCIHBAUD.bit.BAUD = (baud_bits & 0xFF00) >> 8;
	(*sci_regs_ptr).SCILBAUD.bit.BAUD = (baud_bits & 0x00FF);
    
    //Enable Tx/Rx & Tx/Rx ISR
    SciRxSet(sci_regs_ptr, ENABLED);
    SciRxIsrSet(sci_regs_ptr, ENABLED);
    
    SciTxSet(sci_regs_ptr, ENABLED);
    SciTxIsrSet(sci_regs_ptr, ENABLED);

	(*sci_regs_ptr).SCICTL1.bit.SWRESET = 1;  // Relinquish SCI from Reset
    
    //SciTxIsrConfig();
    //SciRxIsrConfig();
}

