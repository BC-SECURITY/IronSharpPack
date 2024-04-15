# IronSharpPack
<p align="center">
	<img src="https://github.com/BC-SECURITY/Empire/assets/42596432/a0e1b1be-a0c8-4212-bc85-4e12ae681130" alt="IronSharpPack" width="300"/>
</p>
IronSharpPack is a repo of popular C# projects that have been emmbeded into IronPython scripts that execute an AMSI bypass then reflective load the C# project. IronPython and the DLR has very little if any instrumentation that makes it an effective language for execution of these assemblies. It was inspired by S3cur3Th1sSh1t's popular [PowerSharpPack](https://github.com/S3cur3Th1sSh1t/PowerSharpPack) project. The C# assemblies were pulled from Flangvik's [Sharp Collection](https://github.com/Flangvik/SharpCollection).

The project also includes IronEmbed which is a script that will automatically compress and embed .NET assemblies into the script wrapper. Any .NET assmebly can be used as long as it has a Main or MainString function. MainString must be a public function but public or private Main functions are supported.  
## Usage
After cloning down the repo all files in the Framework folders are ready to be used with IronPython. They are executed with IronPython and arguments are passed as if running the assembly normally
Example:
	`ipy .\IronSeatbelt.py Antivirus`

If you have an assembly that you would like to use that is not included in the repo it can be embedded with IronEmbed.py. Run IronEmbed by passing the folder the assembly is in as an argument. IronEmbed will convert all exes and dlls in the folder.  
Example:
	`ipy .\IronEmbed.py C:\Users\User\SharpCollection\NetFramework_4.0_Any`
