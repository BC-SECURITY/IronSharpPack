# IronSharpPack
<p align="center">
	<img src="https://github.com/BC-SECURITY/Empire/assets/42596432/a0e1b1be-a0c8-4212-bc85-4e12ae681130" alt="IronSharpPack" width="300"/>
</p>
IronSharpPack is a repo of popular C# projects that have been embedded into IronPython scripts that execute an AMSI bypass and then reflective load the C# project. IronPython and the DLR have very little, if any, instrumentation that makes it an effective language for the execution of these assemblies. It was inspired by S3cur3Th1sSh1t's popular <a href="https://github.com/S3cur3Th1sSh1t/PowerSharpPack"> PowerSharpPack</a> project. The C# assemblies were pulled from Flangvik's <a href="https://github.com/Flangvik/SharpCollection">Sharp Collection</a>.<br><br>

The project also includes IronEmbed, a script that automatically compresses and embeds .NET assemblies into the script wrapper. Any .NET assembly can be used as long as it has a Main or MainString function. MainString must be a public function, but public or private Main functions are supported.  

## Prerequisites 

You must run the scripts with an embedded C# assembly (i.e., anything in one of the NetFramework folders) with the IronPython 3.4 interpreter, but IronEmbed can be run with regular Python on any OS. 
If you are looking for the IronPython installer, it can be found <a href="https://github.com/IronLanguages/ironpython3/releases/tag/v3.4.1">here</a>.

## Usage 

### Execution
After cloning down the repo, all files in the NetFramework folders are ready to be used with IronPython. They are executed with IronPython 3.4 and arguments are passed as if running the assembly normally.

Example:
```
ipy .\IronSeatbelt.py Antivirus
```

### Generating Scripts

If you want to use an assembly that is not included in the repo, you can embed it with IronEmbed.py. Run IronEmbed by passing the folder the assembly is in as an argument. IronEmbed will then convert all exes and dlls in the folder.  

#### Examples

On Windows with IronPython
```
ipy .\IronEmbed.py C:\Users\User\SharpCollection\NetFramework_4.0_Any
```

On Linux with Python
```
python3 IronEmbed.py /path/to/SharpCollection\NetFramework_4.0_Any
```
