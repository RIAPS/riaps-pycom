/*
 * FreeModbus Libary: MSP430 Port
 * Copyright (C) 2006 Christian Walter <wolti@sil.at>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * File: $Id: porttimer.c,v 1.3 2007/06/12 06:42:01 wolti Exp $
 */

/* ----------------------- Platform includes --------------------------------*/
#include "port.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include "mb.h"
#include "mbport.h"
/* --------------------------------------------------------------------------*/
#pragma CODE_SECTION(vMBPortTimersEnable, "ramfuncs");
#pragma CODE_SECTION(CpuTimer0IsrHandler, "ramfuncs");
/* ----------------------- Start implementation -----------------------------*/

/*
*******************************************************************************
* BOOL xMBPortTimersInit(USHORT usTim1Timeout50us)
*******************************************************************************
* Input         : void
* Output        : void
* Description   :
*******************************************************************************
*/

BOOL xMBPortTimersInit(USHORT usTim1Timeout50us)
{
    unsigned long timer_prd_count = usTim1Timeout50us * (unsigned long)50;
    ConfigCpuTimer(&CpuTimer0, 200, timer_prd_count);

    vMBPortTimersEnable();

    return TRUE;
}

void vMBPortTimersEnable( void )
{
    CpuTimer0Regs.TCR.bit.TRB = 1;
    CpuTimer0Regs.TCR.bit.TSS = 0;
}

void vMBPortTimersDisable( void )
{
    CpuTimer0Regs.TCR.bit.TSS = 1;
}

interrupt void CpuTimer0IsrHandler(void)
{
   CpuTimer0.InterruptCount++;
   // Acknowledge this interrupt to receive more interrupts from group 1
   ( void )pxMBPortCBTimerExpired(  );
   PieCtrlRegs.PIEACK.all |= PIEACK_GROUP1;
}



