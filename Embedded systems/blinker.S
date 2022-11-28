
//ARM INSTRUCTIONS
//Instructions are conditional
//32-bit instruction


//How to load data from memory:
//LDR R0, =variable 	(Load address to register. You can use any global variable defined in main.c, or variable found here)
//LDR R1, [R0] 			(Load data from address, in this case 32-bit data)
//LDRB R1, [R0] 		(Load data from address, in this case 8-bit data)
//******
//LDR R0, =0x123456		(Load address to register, Use only if you know the memory address)
//LDR R1, [R0]			(load data from address, in this case 32-bit data)
//LDRB R1, [R0]			(load data from address, in this case 8-bit data)

//How to store data to memory:
//STR R1,[R0]			(R1 contains the data and R0 contains the address where  to store, 32-bit)
//STRB R1,[R0]			(R1 contains the data and R0 contains the address where  to store, 8-bit)


.data
	dir: .byte 1		//8-bit variable for direction
	                    // Add position here


.text

.global blinker


blinker:

	push {r0}				//Push used register to stack

	mov r1, #0x0
	movt r1, #0x4120
	// Delay time in the led changing
	movw r9,#500
// Start the main loop
l1:
	// Set the btn3 led location
	mov r2,#0b1000
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	// Start loop with the first led and compare to the setted delay time.
	s1:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s1

	// Second led location
	mov r2,#0b0100
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	// Second delay comparison loop
	s2:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s2

	// Do the same for the third led.
	mov r2,#0b0010
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	s3:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s3

	// Last led location and looping
	mov r2,#0b0001
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	s4:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s4

	// Third led looping again, coming back
	mov r2,#0b0010
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	s5:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s5

	// Second led again
	mov r2,#0b0100
	strb r2,[r1]
	mov     r3, #0
	movt    r3, #63728
	ldr     r4, [r3, #+516]
	ldr     r5, [r3, #+512]
	lsr		r5, r5, #16
	lsl		r4, r4, #16
	add     r6, r4, r5
	s6:
		ldr     r4, [r3, #+516]
		ldr     r5, [r3, #+512]
		lsr		r5, r5, #16
		lsl		r4, r4, #16
		add     r7, r4, r5
		sub		r8, r7, r6
		cmp		r8, r9
		blt		s6

	b l1// start loop again

	pop {r0}				//Pop register from stack, Remember the pop order if used more than one register (first pushed, last popped)
	bx lr					//Return to place where this function has been called.




