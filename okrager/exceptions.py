class OkragerException(Exception):
    pass

class DatFileCRCHeaderInvalidException(OkragerException):
    def __init__(self, header, message = None):
        """Exception raised when a dat file CRC header was invalid.

        Args:
            header (str): The 4 byte header which was found.
            message (string, optional): A custom message to be displayed in the exception. Defaults to None.
        """
        self.header = header

        message = message if message != None else f'Invalid dat file CRC header. Expecting "!crc"'
        super().__init__(message)