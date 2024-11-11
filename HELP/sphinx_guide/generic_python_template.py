#---------------------------------- FILE INFO ---------------------------------#
#                                                                              #
# Project       : Project Name                                                 #
# Filename      : module_z.py                                                  #
# Author        : team name                                                    #
# Revision      : 1.0                                                          #
# Updated       : yyyy-mm-dd                                                   #
#                                                                              #
# This file contains...                                                        #
#                                                                              #
#-------------------------------- END FILE INFO -------------------------------#

#----------------------------- SPHINX FILE HEADER -----------------------------#
"""
module_z.py

<Insert description of module>.
"""
#--------------------------- END SPHINX FILE HEADER ---------------------------#

#------------------------------------------------------------------------------#
#                                Import Files                                  #
#------------------------------------------------------------------------------#
import module_x
import module_y

#------------------------------------------------------------------------------#
#                                  Definitions                                 #
#------------------------------------------------------------------------------#
__all__ = ['PublicExceptionNameError', 'SomeClass', 'read_memory_location']

# This defines the delimiter to use for parameter parsing
DELIMITER = ','
# This defines the maximum message length
MAX_MSG_SIZE = 255

#------------------------------------------------------------------------------#
#                          Local Conditional Switches                          #
#------------------------------------------------------------------------------#
DEBUG_TRACE = 0 # Nonzero = Enable Debug Trace Output

#------------------------------------------------------------------------------#
#                               Global Variables                               #
#------------------------------------------------------------------------------#
g_kernel_mod_ver: int = 0
g_msgBufs = [
    [0 for _ in range (MAX_INTERFACES)] for _ in range(MAX_MSG_SIZE)
]

#------------------------------------------------------------------------------#
#                               Public Exceptions                              #
#------------------------------------------------------------------------------#
# Public Exceptions
class PublicExceptionNameError(Exception):
    """
    Exception raised for <Insert description here>

    <Insert full description here>

    Attributes:
        balance (float): The current balance in the account.
        amount (float): The amount that was attempted to be withdrawn.

    Args:
        balance (float): The balance available in the account.
        amount (float): The amount that the user attempted to withdraw.
    """

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Can't withdraw {amount}- only {balance} available")

#------------------------------------------------------------------------------#
#                      Private Exceptions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
# Private Exceptions
class _PrivateExceptionNameError(Exception):
    """
    Exception raised for <Insert description here>

    <Insert full description here>
    """

    #no need for definition if we can just go w/ a regular Exeption class's 
    #signature
    pass

#------------------------------------------------------------------------------#
#                                Public Classes                                #
#------------------------------------------------------------------------------#
class SomeClass:
    """
    <Insert brief class description>

    <Insert full class description>

    Attributes:
        attribute1 (int): <Description of attribute1>
        attribute2 (str): <Description of attribute2>
    """

    def __init__(self, attribute1, attribute2):
        """
        Initializes the MyClass instance.

        Args:
            attribute1 (int): <Description of the first attribute>
            attribute2 (str): <Description of the second attribute>
        """
        self.attribute1 = attribute1
        self.attribute2 = attribute2

    def my_method(self, param1, param2):
        """
        <Insert brief method description>

        Args:
            param1 (int): <Description of the first parameter>
            param2 (str): <Description of the second parameter>

        Returns:
            (bool): <Description of return value>
        
        Raises:
            ValueError: <Description of error raised>
        """

        if not isinstance(param1, int):
            raise ValueError("param1 must be an integer")
        if not isinstance(param2, str):
            raise ValueError("param2 must be a string")

        # <Insert code here>

        return True


#------------------------------------------------------------------------------#
#                        Private Classes (DO NOT EXPORT)                       #
#------------------------------------------------------------------------------#
class _NaiPrivateClass:
    """
    <Insert brief class description>

    <Insert full class description here>

    Attributes:
        attribute1 (int): <Description of attribute1>
        attribute2 (str): <Description of attribute2>
    """

    def __init__(self, attribute1, attribute2):
        """
        Initializes the MyClass instance.

        Args:
            attribute1 (int): <Description of the first attribute>
            attribute2 (str): <Description of the second attribute>
        """
        self.attribute1 = attribute1
        self.attribute2 = attribute2

    def _my_method(self, param1, param2):
        """
        <Insert brief method description>

        Args:
            param1 (int): <Description of the first parameter>
            param2 (str): <Description of the second parameter>

        Returns:
            (bool): <Description of return value>
        
        Raises:
            ValueError: <Description of error raised>
        """

        if not isinstance(param1, int):
            raise ValueError("param1 must be an integer")
        if not isinstance(param2, str):
            raise ValueError("param2 must be a string")

        # <Insert code here>

        return True

#------------------------------------------------------------------------------#
#                                Public Functions                              #
#------------------------------------------------------------------------------#
def read_memory_location(
    argLocation, argOffset, p_outValues, argCount, argStride):
    """
    Read unsigned 8-bit values at memory location

    Args:
        argLocation  (mod_x_class):  Memory location
        argOffset    (mod_y_class):  Address offset
        p_outValues  (list)       :  Return array
        argCount     (mod_y_class):  Count
        argStride    (mod_y_class):  Number of memory locations in bytes
    
    Raises:
        PublicExceptionNameError: trying to read 0 bytes

    Returns:
        tmpStatusReturn (naibsp_memory_status_t): Return status
    """
    tmpStatusReturn: naibsp_memory_status_t = NAIBSP_MEMORY_STATUS_NONE
    
    if count == 0:
        raise PublicExceptionNameError(argLocation, count)
        #^use of error isn't consistent w/ the example def but we get the point

    # <Insert code here>
    
    return tmpStatusReturn

#------------------------------------------------------------------------------#
#                       Private Functions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
def _modify_string(p_str):
    """
    Returns the string w/ special characters (\r, \n) removed

    Raises:
        _PrivateExceptionNameError: some reason here

    Args:
        p_str (string): String to adjust

    Returns:
        retValue (int): The length of the string after adjustment
    """
    retValue: int = 0
    
    # <Insert code here>
    raise _PrivateExceptionNameError()
    
    return retValue

#------------------------------------------------------------------------------#
#                                     MAIN                                     #
#------------------------------------------------------------------------------#
def main():
    # <Insert code here>
    

# Example usage
if __name__ == "__main__":
    main()
