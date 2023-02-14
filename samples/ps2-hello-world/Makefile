# Addresses
TEXT	?= 0x400000
DATA	?= 0x3d8000
ABI		?= 0x3d0000

# Variables
SYSTEM          ?= PCSX2

# Binaries
PREFIX	= mips64r5900el-ps2-elf-
CPP		= $(PREFIX)g++
OKRAGER	= okrager

# Directories
BDIR = bin
ODIR = build
SDIR = src

# Files
CPPFILES	= $(wildcard $(SDIR)/*.cpp $(SDIR)/*/*.cpp)
OBJS		= $(patsubst $(SDIR)/%.cpp, $(ODIR)/%.o, $(CPPFILES))

# Save files
ifeq ($(SYSTEM), PCSX2)
	SAVE_IN		?= $(BDIR)/clean/Mcd001.ps2
	SAVE_OUT	?= $(BDIR)/$(SYSTEM)/Mcd001.ps2
else ifeq ($(SYSTEM), $(filter $(SYSTEM),PS4 PS5))
	SAVE_IN		?= $(BDIR)/clean/VMC0.card
	SAVE_OUT	?= $(BDIR)/$(SYSTEM)/VMC0.card
endif

# Flags
LINKFLAGS	= -Wl,-z,max-page-size=0x1,--section-start=.MIPS.abiflags=$(ABI)
CPPFLAGS	= -Tdata=$(DATA) -Ttext=$(TEXT) -mno-gpopt -nostartfiles -nostdlib -nodefaultlibs -ffreestanding $(LINKFLAGS) -I. -D$(SYSTEM)=1

# Target
TARGET = $(shell basename $(CURDIR))-$(SYSTEM).elf

all: compile save

save: $(SAVE_IN) $(SAVE_OUT)
	$(OKRAGER) $(SAVE_IN) $(SAVE_OUT) $(BDIR)/$(TARGET)

compile: $(ODIR) $(BDIR) $(OBJS) crt0
	$(CPP) $(CPPFLAGS) $(ODIR)/crt0.o $(OBJS) -o $(BDIR)/$(TARGET)

crt0:
	$(CPP) $(CPPFLAGS) -c $(SDIR)/crt0.S -o $(ODIR)/crt0.o

$(ODIR)/%.o: $(SDIR)/%.cpp
	@mkdir -p $(shell dirname $@)
	$(CPP) -c -o $@ $< $(CPPFLAGS)

$(BDIR) $(ODIR) $(SAVE_IN) $(SAVE_OUT):
	@mkdir -p $(shell dirname $@)

.PHONY: clean
clean:
	rm -rf $(BDIR)/$(TARGET) $(ODIR) $(BDIR)/$(SYSTEM)