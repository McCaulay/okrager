#include <cstdint>

typedef char* fStrncpy(char* destination, const char* source, unsigned int num);
typedef int   fStrlen(const char* str);

fStrncpy* strncpy = (fStrncpy*)0x001f1e60;
fStrlen* strlen = (fStrlen*)0x001f1b70;

// Okage (System Dynamic)
#if (defined(PCSX2) && PCSX2)
    #define OKAGE_SCREEN_LOAD_NAME     0x008B8C40
    #define OKAGE_SCREEN_LOAD_LOCATION 0x008B99C0
#elif ((defined(PS4) && PS4) || (defined(PS5) && PS5))
    #define OKAGE_SCREEN_LOAD_NAME     0x008B8B10
    #define OKAGE_SCREEN_LOAD_LOCATION 0x008B98A0
#endif

extern "C"
{
    void* memset(void* str, int c, int n)
    {
        for (int i = 0; i < n; i++)
            *((uint8_t*)str + i) = (uint8_t)c;
        return str;
    }
}

void main()
{
    #if (defined(PS4) && PS4)
    const char* system = "Hello PS4!\\n";
    #elif (defined(PS5) && PS5)
    const char* system = "Hello PS5!\\n";
    #elif (defined(PCSX2) && PCSX2)
    const char* system = "Hello PCSX2!\\n";
    #endif

    // Change load name
    strncpy((char*)(OKAGE_SCREEN_LOAD_NAME), "\\f[2]Twitter\x81""F@_mccaulay", 25);

    // Move location text to read-able area
    strncpy((char*)(OKAGE_SCREEN_LOAD_LOCATION), "\\n\\n", 4);

    // Clear previous location overflow text
    memset((char*)(OKAGE_SCREEN_LOAD_LOCATION + 4), 0x00, 0x160);

    // Set system string
    strncpy((char*)(OKAGE_SCREEN_LOAD_LOCATION + 4), system, strlen(system));
}