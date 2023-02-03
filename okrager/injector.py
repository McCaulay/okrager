import struct
from okrager.logger import Logger, Verbosity
from okrager.crc import CRC
from okrager.exceptions import DatFileCRCHeaderInvalidException

class Injector:
    # The player's name is at the following offset within bkmo{i}.dat
    NAME_OFFSET = 0x844

    # The stage 1 shellcode is copied to memory at the folowing address
    SHELLCODE_ADDRESS = 0x01ffe9b4

    # The number of stack variable bytes we must overwrite before overwriting the return address
    STACK_VARIABLE_SIZE = 389

    @staticmethod
    def inject(data, stage1, stage2):
        """Inject the two stager payloads into the bkmo{i}.dat file after the player's name.

        Args:
            data   (bytes): The original input bkmo{i}.dat file contents.
            stage1 (bytes): The PS2 MIPS stage 1 (no NULL byte) shellcode.
            stage2 (bytes): The PS2 MIPS stage 2 (NULL bytes allowed) shellcode.

        Raises:
            DatFileCRCHeaderInvalidException: Exception raised when a dat file CRC header was invalid.

        Returns:
            bytes: The modified bkmo{i}.dat file contents.
        """
        header = data[0:12]
        body = data[12:]

        # Check magic
        if header[0:4] != b'!crc':
            raise DatFileCRCHeaderInvalidException(header[0:4])

        # Set new bkmo{i}.dat body with player's name replaced with payload
        payload = Injector.modifyName(stage1, stage2)
        body = body[:Injector.NAME_OFFSET] + payload + body[Injector.NAME_OFFSET+len(payload):]

        # Update CRC checksum of modified body contents
        checksum = CRC.calculate(body)
        Logger.info(Verbosity.DEBUG, f'CRC: 0x{checksum:08x}')
        header = header[0:8] + struct.pack('<I', checksum)

        return header + body

    @staticmethod
    def modifyName(stage1, stage2):
        """Modify the player's name to overflow the stack and gain code execution.

        Args:
            stage1 (bytes): The initial stage shellcode to execute.
            stage2 (bytes): The second stage shellcode to execute.

        Returns:
            bytes: The modified player's name overriding the return address and appending the stager payloads.
        """
        variables = b'A' * Injector.STACK_VARIABLE_SIZE
        pc = struct.pack('<I', Injector.SHELLCODE_ADDRESS)
        Logger.info(Verbosity.DEBUG, f'PC: 0x{Injector.SHELLCODE_ADDRESS:08x}')

        # Padding alignment for shellcode
        padding = b"\x00\x00\x00"

        return variables + pc + stage1 + padding + stage2