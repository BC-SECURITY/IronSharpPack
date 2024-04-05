import sys
import os
import base64
import zlib
#helper functions 
def file_to_base64_compressed(file_path):
    with open(file_path, 'rb') as file:

        # Compress the file's binary data
        compressed_data = zlib.compress(file.read())

        # Encode the compressed data to base64
        base64_encoded = base64.b64encode(compressed_data).decode('utf-8')
        return base64_encoded


if sys.argv[1] == 'help':
    print('''IronAssembly compresses a .NET assemblies embeds it into an IronPython script
    arguments should be <assembly_directory>''')

else:	
    for filename in os.listdir(sys.argv[1]):
        if filename.endswith('.exe'):
            compressed_assembly = file_to_base64_compressed(sys.argv[1])
            with open('IronSharpPack_template.py', 'r') as file:
                script = file.read()
                script = script.replace("<replace>", compressed_assembly)
            out_name = "Iron" + filename
            with open(out_name, 'w') as out_file:
                out_file.write(script)
                
        

