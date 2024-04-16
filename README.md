# IronSharpPack
<p align="center">
	<img src="https://github.com/BC-SECURITY/Empire/assets/42596432/a0e1b1be-a0c8-4212-bc85-4e12ae681130" alt="IronSharpPack" width="300"/>
</p>
IronSharpPack is a repo of popular C# projects that have been embedded into IronPython scripts that execute an AMSI bypass and then reflective load the C# project. IronPython and the DLR have very little, if any, instrumentation that makes it an effective language for the execution of these assemblies. It was inspired by S3cur3Th1sSh1t's popular <a href="https://github.com/S3cur3Th1sSh1t/PowerSharpPack"> PowerSharpPack</a> project. The C# assemblies were pulled from Flangvik's <a href="https://github.com/Flangvik/SharpCollection">Sharp Collection</a>.<br><br>

The project also includes IronEmbed, a script that automatically compresses and embeds .NET assemblies into the script wrapper. Any .NET assembly can be used as long as it has a Main or MainString function. MainString must be a public function, but public or private Main functions are supported.  
## Usage
After cloning down the repo, all files in the Framework folders are ready to be used with IronPython. They are executed with IronPython and arguments are passed as if running the assembly normally

Example:<br>
	`ipy .\IronSeatbelt.py Antivirus`


If you want to use an assembly that is not included in the repo, you can embed it with IronEmbed.py. Run IronEmbed by passing the folder the assembly is in as an argument. IronEmbed will then convert all exes and dlls in the folder.  

Example:<br>
	`ipy .\IronEmbed.py C:\Users\User\SharpCollection\NetFramework_4.0_Any`
