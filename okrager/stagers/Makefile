# Binaries
PREFIX=mips64r5900el-ps2-elf-
CC=$(PREFIX)gcc
OBJCOPY=$(PREFIX)objcopy

# Config
GP=0x03dfff0 # Obtain from: $(PREFIX)readelf -s program.elf | grep '_gp'
CONFIG=okage.cfg

# Flags
LINKFLAGS=-Wl,-z,max-page-size=0x1
CCFLAGS=-nostartfiles -nostdlib -nodefaultlibs -ffreestanding -DGP=$(GP) -include $(CONFIG) $(LINKFLAGS)
COPYFLAGS=$(LINKFLAGS) -O binary

# Stage Names
STAGE1=stage1
STAGE2=stage2

# Output files
STAGE1_ELF=bin/$(STAGE1).elf
STAGE1_BIN=bin/$(STAGE1).bin

STAGE2_ELF=bin/$(STAGE2).elf
STAGE2_TEXT=bin/$(STAGE2).text
STAGE2_DATA=bin/$(STAGE2).data
STAGE2_BIN=bin/$(STAGE2).bin

make:
	$(CC) $(CCFLAGS) -c $(STAGE1).S -o $(STAGE1_ELF)
	$(CC) $(CCFLAGS) -c $(STAGE2).S -o $(STAGE2_ELF)
	$(OBJCOPY) $(COPYFLAGS) --only-section .text $(STAGE1_ELF) $(STAGE1_BIN)
	$(OBJCOPY) $(COPYFLAGS) --only-section .text $(STAGE2_ELF) $(STAGE2_TEXT)
	$(OBJCOPY) $(COPYFLAGS) --only-section .data $(STAGE2_ELF) $(STAGE2_DATA)
	cat $(STAGE2_DATA) > $(STAGE2_BIN)
	cat $(STAGE2_TEXT) >> $(STAGE2_BIN)
	rm $(STAGE1_ELF)
	rm $(STAGE2_ELF)
	rm $(STAGE2_TEXT)
	rm $(STAGE2_DATA)

clean:
	rm $(STAGE1_ELF)
	rm $(STAGE1_BIN)
	rm $(STAGE2_ELF)
	rm $(STAGE2_TEXT)
	rm $(STAGE2_DATA)
	rm $(STAGE2_BIN)