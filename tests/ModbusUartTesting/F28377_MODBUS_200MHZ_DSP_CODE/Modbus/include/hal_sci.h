#ifndef _HAL_SCI_H
#define _HAL_SCI_H


#include "port.h"
#include "F28x_Project.h"
#include "stdbool.h"

void  SciRxSet (volatile struct SCI_REGS* sci_regs_ptr, _Bool value);
void  SciTxSet (volatile struct SCI_REGS* sci_regs_ptr, _Bool value);
void  SciRxIsrSet(volatile struct SCI_REGS* sci_regs_ptr, _Bool value);
void  SciTxIsrSet(volatile struct SCI_REGS* sci_regs_ptr, _Bool value);
void  SciInit(volatile struct SCI_REGS* sci_regs_ptr, Uint32 baudrate);

#endif
