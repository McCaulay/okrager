# Stage 2
# * Restore corrupted callee-saved registers
# * Read program.elf from memory card
# * Load ELF into memory
# * Execute entry
# * Return to stage 1
# * NULL bytes allowed

# Shellcode Variables
.data
.global filename
    filename: .asciiz "BASCUS-97129/program.elf\x00\x00\x00"

.section .text

.global _start
_start:
    # Fix corrupted callee-saved registers
    li $fp, 0x00210000
    li $s0, 0x00250000
    li $s1, 0x0024EEA4
    li $s2, 0x00250000
    li $s3, 0x00250000
    li $s4, 0x0024EE98
    li $s5, 0x00250000
    li $s6, 0x00250000
    li $s7, 0x00250000
    li $sp, 0x01FFE9C0

    # Local stack variables
    # 0x00 - void* gameSave
    # 0x04 - int fd
    # 0x08 - void* elf
    # 0x0C - int size
    # 0x10 - void* programHeaders
    # 0x14 - int programHeaderSize
    # 0x18 - int programHeaderCount
    # 0x1C - int i
    # 0x20 - $ra
    # 0x24 - $fp

    # Function setup
    addiu $sp, $sp, -0x28
    sw $ra, 0x20($sp)
    sw $fp, 0x24($sp)
    move $fp, $sp

    # Variable initialization
    sw $zero, 0x00($sp)
    sw $zero, 0x04($sp)
    sw $zero, 0x08($sp)
    sw $zero, 0x0c($sp)
    sw $zero, 0x10($sp)
    sw $zero, 0x14($sp)
    sw $zero, 0x18($sp)
    sw $zero, 0x1c($sp)

    # Store game save location in gameSave
    lw $t0, 0x0024EE04 # t0 = *gGameSave
    sw $t0, 0x00($sp)  # gameSave = t0 = *gGameSave

    # int fd = MemoryCardOpen("program.elf", 1)
    lw $a0, 0x00($sp)  # a0 = *gGameSave
    addi $a0, 0xA0C    # a0 = *gGameSave + 0xA0C = filename
    li $a1, 1          # a1 = 1
    jal MemoryCardOpen # int fd = MemoryCardOpen("BASCUS-97129/program.elf", 1)
    sw $v0, 0x04($sp)  # fd = v0

    # MemoryCardRead(fd, &size, 4)
    lw $a0, 0x04($sp)  # a0 = fd
    move $a1, $sp
    addi $a1, 0x0C     # a1 = &size
    li $a2, 4          # a2 = 4
    jal MemoryCardRead # MemoryCardRead(fd, &size, 4)

    # elf = malloc(size);
    lw $a0, 0x0C($sp)  # a0 = size
    jal malloc         # char* elf = malloc(size);
    sw $v0, 0x08($sp)  # elf = v0

    # MemoryCardRead(fd, elf, size)
    lw $a0, 0x04($sp)  # a0 = fd
    lw $a1, 0x08($sp)  # a1 = elf
    lw $a2, 0x0C($sp)  # a2 = size
    jal MemoryCardRead # MemoryCardRead(fd, elf, size)

    # MemoryCardClose(fd)
    lw $a0, 0x04($sp)   # a0 = fd
    jal MemoryCardClose # MemoryCardClose(fd)

    # Load ELF into memory
    lw $t0, 0x08($sp)  # t0 = elf

    # Program header table
    lw $t1, 0x1C($t0)    # t1 = *(uint32_t*)(elf + 0x1C) = programHeaderOffset
    add $t1, $t0         # t1 = elf + programHeaderOffset
    sw $t1, 0x10($sp)    # programHeaders = t1

    # Program header size
    lh $t1, 0x2A($t0)    # t1 = *(uint16_t*)(elf + 0x2A) = programHeaderSize
    sw $t1, 0x14($sp)    # programHeaderSize = t1

    # Program header count
    lh $t1, 0x2C($t0)    # t1 = *(uint16_t*)(elf + 0x2C) = programHeaderCount
    sw $t1, 0x18($sp)    # programHeaderCount = t1

    # Load each entry
loadLoop:
    # Get i'th program header
    lw $t1, 0x10($sp)    # t1 = programHeaders
    lw $t2, 0x1c($sp)    # t2 = i
    lw $t3, 0x14($sp)    # t3 = programHeaderSize
    mul $t2, $t3         # t2 = i * programHeaderSize
    add $t2, $t1         # t2 = programHeaders + (i * programHeaderSize) = programHeader

    # memcpy(sectionDestination, sectionSource, sectionSize)
    lw $a0, 0x08($t2)        # a0 = *(uint32_t*)(programHeader + 0x08) = sectionDestination
    lw $a1, 0x04($t2)        # a1 = *(uint32_t*)(programHeader + 0x04) = sectionOffset
    beq $a1, 0, loopContinue # if (sectionOffset != 0)
    add $a1, $t0, $a1        # a1 = elf + sectionOffset
    lw $a2, 0x10($t2)        # a2 = *(uint32_t*)(programHeader + 0x10) = sectionSize
    jal memcpy               # memcpy(sectionDestination, sectionSource, sectionSize)
loopContinue:

    # i++
    lw $t1, 0x1c($sp)  # t1 = i
    addi $t1, 1        # t1++
    sw $t1, 0x1c($sp)  # i = t1

    # i < programHeaderCount
    lw $t2, 0x18($sp)  # t2 = programHeaderCount
    blt $t1, $t2, loadLoop

    # Set gp to _gp
    li $gp, GP

    # Call entry
    lw $t0, 0x08($sp)   # t0 = elf
    lw $t1, 0x18($t0)   # t1 = *(uint32_t*)(elf + 0x18) = entry
    jalr $t1            # entry()

    # Free elf
    lw $a0, 0x08($sp)  # a0 = elf
    jal free           # free(elf);

    # Restore gp
    li $gp, 0

    # Function teardown
    move $sp, $fp
    lw $ra, 0x20($sp)
    lw $fp, 0x24($sp)
    addiu $sp, $sp, 0x28

    # Return to stage 1
    jr $ra