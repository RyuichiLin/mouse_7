/*-------------------------------- FILE INFO ---------------------------------*/
/* Filename           : filename_abc.c                                        */
/* Author             : Team Kirbo                                            */
/* Layer              : abc layer                                             */
/*                                                                            */
/* This file contains...                                                      */
/*                                                                            */
/* (add below if applicable):                                                 */
/* Target Hardware    : AT32UC3L0256                                          */
/* IDE                : Atmel Studio 7.4.2542                                 */
/* SDK                : ASF 3.52.0                                            */
/*----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------*/
/*                               Include Files                                */
/*----------------------------------------------------------------------------*/
//(where xyz is a layer adjacent to abc)
#include "xyz_libraries/layertypes.h"
#include "xyz_libraries/layerlib.h"
#include "xyz_libraries/layerdefs.h"

/*----------------------------------------------------------------------------*/
/*                                Definitions                                 */
/*----------------------------------------------------------------------------*/
//(all private constants here- otherwise NONE)

/* Separator used for <insert use case> in this file */
#define ABC_DELIMITER ','
/* Buffer size for <insert use case> in this file */
#define ABC_BUFFER_SIZE (255)

/*----------------------------------------------------------------------------*/
/*                               Debug Switches                               */
/*----------------------------------------------------------------------------*/
#define ABC_DEBUG_ENABLE 0 /* Nonzero = Enable Debug Output */

/*----------------------------------------------------------------------------*/
/*                              Global Variables                              */
/*----------------------------------------------------------------------------*/
static int32_t g_abc_global_variable_name;
static uint8_t g_abc_global_buffer_name[ABC_BUFFER_SIZE];

/* (if in absolutely need of a global var in a different source file) */
extern int32_t g_some_global_var;

/*----------------------------------------------------------------------------*/
/*                    Private (Static) Function Prototype                     */
/*----------------------------------------------------------------------------*/
/* <Insert brief function purpose here> */
static int32_t abc_PrivateFunctionName(const char* p_pointer_parameter_name);

/*----------------------------------------------------------------------------*/
/*                       Public (Exportable) Functions                        */
/*----------------------------------------------------------------------------*/
/**
* <Insert function description here>
*
* \param[in]  someLocation   Memory location
* \param[in]  someOffset     Address offset
* \param[in]  arrayCount     Array item count
* \param[in]  arrayStride    Bytes between elements in array
* \param[out] p_outputArray  Return array
* \retval ABC_RETURN_STATUS_NONE               None
* \retval ABC_RETURN_STATUS_SUCCESS            Success
* \retval ABC_RETURN_STATUS_INVALID_ACCESS     Failure: Invalid access
* \retval ABC_RETURN_STATUS_INVALID_OFFSET     Failure: Invalid offset
* \retval ABC_RETURN_STATUS_INVALID_LOCATION   Failure: Invalid location
* \retval ABC_RETURN_STATUS_INVALID_PARAMETER  Failure: Invalid parameter
* \retval ABC_RETURN_STATUS_OFFSET_OVERFLOW    Failure: Offset overflow
*/
abc_status_t abc_Read_Memory_Location(
    const abc_memory_location_t someLocation, 
    const abc_size_t someOffset, 
    const abc_size_t arrayCount,
    const abc_size_t arrayStride,
    uint8_t* const p_outputArray)
{
    abc_status_t returnStatus = ABC_RETURN_STATUS_NONE;
    
    /* code */
    
    return returnStatus;
}

/*----------------------------------------------------------------------------*/
/*                         Private (Static) Functions                         */
/*----------------------------------------------------------------------------*/
/**
* <insert function description here>
*
* \param[in] p_pointer_parameter_name Some pointer parameter
* \returns Description of return value in a broad sense
*/
static int32_t abc_PrivateFunctionName(const char* p_pointer_parameter_name)
{
    int32_t retValue = 0;

    /* code */
    
    return retValue;
}






/*----------------------------------------------------------------------------*/
/*                                    Main                                    */
/*----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------*/
/*                         Interrupt Service Routines                         */
/*----------------------------------------------------------------------------*/