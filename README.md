# okrager

## Overview
The "okrager" console application allows you to generate an exploitable [Okage: Shadow King](https://en.wikipedia.org/wiki/Okage:_Shadow_King) game save which will leverage a stack buffer-overflow vulnerability within the player's name in the save file. This results in the code execution of the supplied PS2 ELF file when you select "RESTORE GAME" within the [Okage: Shadow King](https://en.wikipedia.org/wiki/Okage:_Shadow_King) game.

The application requires you to pass an existing input memory card file (.ps2/.card). Next, it injects the staging shellcode and the supplied PS2 ELF then saves the game save as a new output file (.ps2/.card).

For additional information on the inner working of this application, see the assosicated blog post "[mast1c0re: Part 2 - Arbitrary PS2 code execution](https://mccaulay.co.uk/mast1c0re-part-2-arbitrary-ps2-code-execution/)".

## Installation

Use the following command to install the okrager package with pip:

~~~
python -m pip install okrager
~~~

Make sure the local bin path is in your path. If not, add it to `~/.bashrc` or `~/.zshrc`:

~~~sh
export PATH="$HOME/.local/bin:$PATH"
~~~

## Usage

~~~
usage: okrager [-h] [-c CODE] [-s1 STAGE1] [-s2 STAGE2] [-v {none,normal,debug}] input output elf

Generate an Okage Shadow King exploitation game save.

positional arguments:
  input                 The input .ps2/.card game save file.
  output                The exported .ps2/.card game save file.
  elf                   The compiled PS2 ELF filepath to inject.

optional arguments:
  -h, --help            show this help message and exit
  -c CODE, --code CODE  The game save identifier code. (Default: BASCUS-97129)
  -s1 STAGE1, --stage1 STAGE1
                        The stage 1 shellcode to be executed.
  -s2 STAGE2, --stage2 STAGE2
                        The stage 2 shellcode to be executed.
  -v {none,normal,debug}, --verbosity {none,normal,debug}
                        The script output verbosity mode. (Default: normal)
~~~

## Examples

### PS4 / PS5
~~~
└─$ okrager VMC0.card VMC0-exploit.card program.elf
[#] Loading stagers and ELF
[#] Loading memory card
[#] Exporting BASCUS-97129
[#] Reading BASCUS-97129.psu
[#] Modifying bkmo0.dat
[#] Writing ELF
[#] Saving BASCUS-97129.psu
[#] Deleting BASCUS-97129
[#] Importing BASCUS-97129.psu
[+] Exploit wrote to save file "VMC0-exploit.card"
~~~

### PCSX2
~~~
└─$ okrager Mcd001.ps2 Mcd001-exploit.ps2 program.elf
[#] Loading stagers and ELF
[#] Loading memory card
[#] Exporting BASCUS-97129
[#] Reading BASCUS-97129.psu
[#] Modifying bkmo0.dat
[#] Writing ELF
[#] Saving BASCUS-97129.psu
[#] Deleting BASCUS-97129
[#] Importing BASCUS-97129.psu
[+] Exploit wrote to save file "Mcd001-exploit.ps2"
~~~

# References
* <https://s3-eu-west-1.amazonaws.com/downloads-mips/documents/MIPS_Architecture_MIPS64_InstructionSet_%20AFP_P_MD00087_06.05.pdf>
* <https://shell-storm.org/online/Online-Assembler-and-Disassembler/>
* <https://github.com/beardypig/ghidra-emotionengine>
* <https://github.com/ps2dev/ps2sdk>
* <https://github.com/ps2dev/ps2toolchain>
* <https://github.com/ps2dev/mymc>
* <https://pypi.org/project/mymcplus/>
* <https://git.sr.ht/~thestr4ng3r/mymcplus>
* <https://playstationdev.wiki/ps2devwiki/index.php/Main_Page>
* <https://www.copetti.org/writings/consoles/playstation-2/>