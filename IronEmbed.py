import sys
import os
import base64
import zlib

def file_to_base64_compressed(file_path):
    with open(file_path, 'rb') as file:
        compressed_data = zlib.compress(file.read())
        base64_encoded = base64.b64encode(compressed_data).decode('utf-8')
        return base64_encoded

def main():
    # Check for minimum required arguments and help command
    if len(sys.argv) < 3 or sys.argv[1] == 'help':
        print('''IronEmbed compresses a .NET assembly and embeds it into an IronPython script
        Usage: python IronEmbed.py <assembly_directory> <output_directory>''')
        return

    assembly_dir = sys.argv[1]
    output_dir = sys.argv[2]
    remove_comments_flag = '--remove-comments' in sys.argv 

    for file_name in os.listdir(assembly_dir):
        if file_name.endswith('.exe') or file_name.endswith('.dll'):
            file_path = os.path.join(assembly_dir, file_name)
            compressed_assembly = file_to_base64_compressed(file_path)

            with open('IronSharpPack_template.py', 'r') as file:
                script = file.read()
                script = script.replace("<replace_assembly>", compressed_assembly)
                script = script.replace("<replace_programname>", file_name.replace('.exe', '').replace('.dll', ''))

            out_name = os.path.join(output_dir, "Iron" + file_name.replace('.exe', '.py').replace('.dll', '.py'))
            with open(out_name, 'w') as out_file:
                out_file.write(script)

if __name__ == "__main__":
    main()
