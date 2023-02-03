import ctypes

class CRC:
    """Python implementation of Okage: Shadow King's calculateCRC game save functionality.

    uint32_t calculateCRC(byte* buffer, int size) = 0x0016d838
    int      gCRCTableInitialized                 = 0x001fde8c
    int16_t  gCRCTable[256]                       = 0x002e27e8
    """
    TABLE_INITIALIZED = False
    TABLE = []

    @staticmethod
    def initialize():
        """Initializes the CRC table with 255 bytes.
        """
        CRC.TABLE_INITIALIZED = True

        for i in range(0, 255):
            value = ctypes.c_uint32(i)
            value.value <<= 8
            for j in range(0, 8):
                if value.value & 0x8000 == 0:
                    value.value <<= 1
                else:
                    value.value <<= 1
                    value.value ^= 0x1021
            CRC.TABLE.append(ctypes.c_uint16(value.value))
        CRC.TABLE.append(ctypes.c_uint16(0))

    @staticmethod
    def calculate(data):
        """Calculates the CRC (Cyclic Redundancy Check) value of the given data.

        Args:
            data (bytes): The input data bytes to calculate the CRC value from.

        Returns:
            int: The unsigned 32-bit integer CRC value.
        """
        if not CRC.TABLE_INITIALIZED:
            CRC.initialize()

        # Calculate checksum
        checksum = ctypes.c_uint32(0xFFFF)
        for i in range(0, len(data)):
            checksumShift = ctypes.c_uint32(checksum.value >> 8)
            preindex = ctypes.c_uint32(ctypes.c_uint32(data[i]).value ^ checksumShift.value)
            index = ctypes.c_uint32(preindex.value & 0xff)
            checksum.value <<= 8
            checksum.value ^= ctypes.c_uint32(CRC.TABLE[index.value].value).value
        checksum.value = ~checksum.value

        return checksum.value
