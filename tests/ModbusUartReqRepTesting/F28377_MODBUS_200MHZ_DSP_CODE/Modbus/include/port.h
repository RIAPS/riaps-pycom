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
 * File: $Id: port.h,v 1.2 2006/11/19 03:36:01 wolti Exp $
 */

#ifndef _PORT_H
#define _PORT_H

/* ----------------------- Platform includes --------------------------------*/

#include "F28x_Project.h"
#include "stdbool.h"
#include "assert.h"
#include "hal_sci.h"
#if defined (__GNUC__)
#include <signal.h>
#endif
#undef CHAR

/* ----------------------- Defines ------------------------------------------*/
#define	INLINE
#define PR_BEGIN_EXTERN_C           extern "C" {
#define	PR_END_EXTERN_C             }

#define ENTER_CRITICAL_SECTION(  )   DINT
#define EXIT_CRITICAL_SECTION(  )    EINT

#if(0)
#define assert( expr )
#endif

typedef _Bool BOOL;

typedef unsigned char UCHAR;
typedef char CHAR;

typedef Uint16 USHORT;
typedef int16 SHORT;

typedef Uint32 ULONG;
typedef int32 LONG;

#ifndef TRUE
#define TRUE            1
#endif

#ifndef FALSE
#define FALSE           0
#endif

#endif

#define ENABLED		TRUE
#define DISABLED 	FALSE

extern interrupt void SciTxIsrHandler(void);

extern interrupt void SciRxIsrHandler(void);

extern interrupt void CpuTimer0IsrHandler(void);
