/*-------------------------------- FILE INFO ---------------------------------*/
/* Filename           : filename_abc.h                                        */
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
#ifndef FILENAME_ABC_H_
#define FILENAME_ABC_H_

/*----------------------------------------------------------------------------*/
/*                                Definitions                                 */
/*----------------------------------------------------------------------------*/
//(all public constants (user defined type/enumerations, etc)- otherwise NONE)

/* <Insert constant description here> */
#define ABC_BUTTON_DEBOUNCE_TIME_MS (10u)

/* <Insert user defined type description here> */
typedef enum 
{
    MCI_BUTTON_NOT_PRESSED = 0u,
    MCI_BUTTON_PRESSED
} mci_button_pressed_t;

/*----------------------------------------------------------------------------*/
/*                              Global Variables                              */
/*----------------------------------------------------------------------------*/
//(usually NONE- don't spread access to global variables w/ header files)

/*----------------------------------------------------------------------------*/
/*                       Public (Exportable) Functions                        */
/*----------------------------------------------------------------------------*/
/* Public function prototypes here */
abc_status_t abc_Read_Memory_Location(
    const abc_memory_location_t someLocation, 
    const abc_size_t someOffset, 
    const abc_size_t arrayCount,
    const abc_size_t arrayStride,
    uint8_t* const p_outputArray);

#endif /* FILENAME_ABC_H_ */