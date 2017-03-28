/*
 * FreeModbus Libary: MSP430 Demo Application
 * Copyright (C) 2006 Christian Walter <wolti@sil.at>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * File: $Id: demo.c,v 1.3 2006/11/19 15:22:40 wolti Exp $
 */

/* ----------------------- Platform includes --------------------------------*/
#include "port.h"
#include "string.h"

/* ----------------------- Modbus includes ----------------------------------*/
#include "mb.h"
#include "mbport.h"
#include "mb_interface.h"


/* ----------------------- Defines ------------------------------------------*/
#define MB_SLAVE_ID						(0x0A)
#define MB_BAUD_RATE					(57600)

#define REG_INPUT_START   				(0)
#define REG_INPUT_NREGS   				(6U)

#define REG_HOLDING_START 				(0)
#define REG_HOLDING_NREGS 				(4U)


/* ----------------------- Static variables ---------------------------------*/
static USHORT   usRegInputStart = REG_INPUT_START;
static USHORT   usRegInputBuf[REG_INPUT_NREGS];
static USHORT   usRegHoldingStart = REG_HOLDING_START;
static USHORT   usRegHoldingBuf[REG_HOLDING_NREGS];
eMBErrorCode    eStatus;


//information exchange between main and modbus
volatile USHORT test_rx_from_master;
extern volatile float Pref;
extern volatile int Active;

static void MBUpdateData(void);
/* ----------------------- Start implementation -----------------------------*/

/*
*******************************************************************************
* void ModbusInit(void)
*******************************************************************************
* Input         : void
* Output        : void
* Description   : Main Function for HUPS project.
*******************************************************************************
*/

void ModbusInit(void)
{
	eStatus = eMBInit(MB_RTU, MB_SLAVE_ID, 0, MB_BAUD_RATE, MB_PAR_NONE);
	eStatus = eMBEnable();
	//Initialize all the registers to zero
	memset(usRegHoldingBuf, 0, sizeof(usRegHoldingBuf));
	memset(usRegInputBuf, 0, sizeof(usRegInputBuf));


}// End of ModbusInit


/*
*******************************************************************************
* void ModbusPoll(void)
*******************************************************************************
* Input         : void
* Output        : void
* Description   :
*******************************************************************************
*/

void ModbusPoll(void)
{
	MBUpdateData();
	(void)eMBPoll();
}// End of ModbusPoll

/*
*******************************************************************************
* eMBErrorCode eMBRegHoldingCB( UCHAR * pucRegBuffer, USHORT usAddress,
* 								USHORT usNRegs, eMBRegisterMode eMode )
*******************************************************************************
* Input         : void
* Output        : void
* Description   :
*******************************************************************************
*/

void MBUpdateData(void)
{
	//Because of the way the MODBUS protocol is defined, the index locations '0' for usRegInputBuf and usRegHoldingBuf shall be unutilized.
	//Thus in the example below, usRegInputBuf[0], though assigned a value of 20 in the code here, doesn't make any difference as far as the Modbus Master is concerned.
	//Modbus Master will never be able to poll for usRegInputBuf[0]. Hence the assignment here is redundant.

	usRegInputBuf[0] 		= 20; // this useless as mentioned above

	usRegInputBuf[1] 		= 1; // this is to store the output current

	usRegInputBuf[2] 		= 2; // this is to store the output voltage

	usRegInputBuf[3] 		= 3; // this is to store the phase of voltage

	usRegInputBuf[4] 		= 4; // this is to store the time


	test_rx_from_master =  usRegHoldingBuf[1]; // this is the start and stop command
	Active = usRegHoldingBuf[1];
	test_rx_from_master =  usRegHoldingBuf[2]; // this is the POWER command
	Pref = usRegHoldingBuf[2];
}// End of MBUpdateData


/*
*******************************************************************************
* eMBErrorCode eMBRegInputCB( UCHAR * pucRegBuffer, USHORT usAddress, USHORT usNRegs )
*******************************************************************************
* Input         : void
* Output        : void
* Description   :
*******************************************************************************
*/

eMBErrorCode eMBRegInputCB( UCHAR * pucRegBuffer, USHORT usAddress, USHORT usNRegs )
{
    eMBErrorCode    eStatus = MB_ENOERR;
    int             iRegIndex;

    if( ( usAddress >= REG_INPUT_START )
        && ( usAddress + usNRegs <= REG_INPUT_START + REG_INPUT_NREGS ) )
    {
        iRegIndex = ( int )( usAddress - usRegInputStart );
        while( usNRegs > 0 )
        {
            *pucRegBuffer++ = ( unsigned char )( usRegInputBuf[iRegIndex] >> 8 );
            *pucRegBuffer++ = ( unsigned char )( usRegInputBuf[iRegIndex] & 0xFF );
            iRegIndex++;
            usNRegs--;
        }
    }
    else
    {
        eStatus = MB_ENOREG;
    }

    return eStatus;
}


/*
*******************************************************************************
* eMBErrorCode eMBRegHoldingCB( UCHAR * pucRegBuffer, USHORT usAddress,
* 								USHORT usNRegs, eMBRegisterMode eMode )
*******************************************************************************
* Input         : void
* Output        : void
* Description   :
*******************************************************************************
*/

eMBErrorCode eMBRegHoldingCB( UCHAR * pucRegBuffer, USHORT usAddress,
							  USHORT usNRegs, eMBRegisterMode eMode )
{
    eMBErrorCode    eStatus = MB_ENOERR;
    int             iRegIndex;

    if( ( usAddress >= REG_HOLDING_START ) &&
        ( usAddress + usNRegs <= REG_HOLDING_START + REG_HOLDING_NREGS ) )
    {
        iRegIndex = ( int )( usAddress - usRegHoldingStart );
        switch ( eMode )
        {
            /* Pass current register values to the protocol stack. */
        case MB_REG_READ:
            while( usNRegs > 0 )
            {
                *pucRegBuffer++ = ( unsigned char )( usRegHoldingBuf[iRegIndex] >> 8 );
                *pucRegBuffer++ = ( unsigned char )( usRegHoldingBuf[iRegIndex] & 0xFF );
                iRegIndex++;
                usNRegs--;
            }
            break;

            /* Update current register values with new values from the
             * protocol stack. */
        case MB_REG_WRITE:
            while( usNRegs > 0 )
            {
                usRegHoldingBuf[iRegIndex] = *pucRegBuffer++ << 8;
                usRegHoldingBuf[iRegIndex] |= *pucRegBuffer++;
                iRegIndex++;
                usNRegs--;
            }
        }
    }
    else
    {
        eStatus = MB_ENOREG;
    }
    return eStatus;
}

eMBErrorCode
eMBRegCoilsCB( UCHAR * pucRegBuffer, USHORT usAddress, USHORT usNCoils, eMBRegisterMode eMode )
{
    return MB_ENOREG;
}

eMBErrorCode
eMBRegDiscreteCB( UCHAR * pucRegBuffer, USHORT usAddress, USHORT usNDiscrete )
{
    return MB_ENOREG;
}
