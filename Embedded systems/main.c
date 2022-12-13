/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 *
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

// Main program for exercise

//****************************************************
//By default, every output used in this exercise is 0
//****************************************************
#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "sleep.h"
#include "xgpiops.h"
#include "xttcps.h"
#include "xscugic.h"
#include "xparameters.h"
#include "Pixel.h"
#include "Interrupt_setup.h"


//********************************************************************
//***************TRY TO READ COMMENTS*********************************
//********************************************************************

//***Hint: Use sleep(x)  or usleep(x) if you want some delays.****
//***To call assembler code found in blinker.S, call it using: blinker();***


//Comment this if you want to disable all interrupts
#define enable_interrupts

// Predefining the functions to prevent compiler warning "Conflicting type"
void check_lazer_hit();
void reset_variables();
void menu_screen();
void generate_alien();
void move_alien();
void check_alien_hit();
void clear_matrix();
void draw_alien();
void draw_ship();
void draw_symbols_to_matrix(uint8_t matrix[]);
void draw_lazer();

// Define used variables and initialize them
uint8_t channel_pointer = 0;
uint8_t game_over = 1;
uint8_t ship_location = 2;
uint8_t alien_x = 0;
uint8_t alien_y = 0;
uint8_t alien_direction = 0;
uint8_t move_freq_val = 200;
uint8_t alien__move_freq_rate = 200;
uint8_t lazer_x = 0;
uint8_t lazer_y = 0;
uint8_t points = 0;

uint8_t text[][8] ={
				//alien
				 {0b00011000,
				 0b00111100,
				 0b01111110,
				 0b11011011,
				 0b11111111,
				 0b00100100,
				 0b01011010,
				 0b10100101},
				 // Number 0
				{0b1110,
				 0b1010,
				 0b1010,
				 0b1010,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 //Number 1
			    {0b0110,
				 0b0100,
				 0b0100,
				 0b0100,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 // Number 2
				{0b1110,
				 0b1000,
				 0b1110,
				 0b0010,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 //Number 3
				{0b1110,
				 0b1000,
				 0b1110,
				 0b1000,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 // Number 4
				{0b1010,
				 0b1010,
				 0b1110,
				 0b1000,
				 0b1000,
				 0b0000,
				 0b0000,
				 0b0000},
				// Number 5
				 {0b1110,
				 0b0010,
				 0b1110,
				 0b1000,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 // Number 6
				{0b1110,
				 0b0010,
				 0b1110,
				 0b1010,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				 //Number 7
				{0b1110,
				 0b1000,
				 0b1000,
				 0b1000,
				 0b1000,
				 0b0000,
				 0b0000,
				 0b0000},
				 // Number 8
				{0b1110,
				 0b1010,
				 0b1110,
				 0b1010,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000},
				// Number 9
				 {0b1110,
				 0b1010,
				 0b1110,
				 0b1000,
				 0b1110,
				 0b0000,
				 0b0000,
				 0b0000}};
/***************************************************************************************
Name: Ville Tiljander
Student number: H274523

Name: Toivo Wuoti
Student number: H281977

Name:
Student number:

Tick boxes that you have coded

Led-matrix driver		Game		    Assembler
	[X]					[X]					[]

Brief description:

*****************************************************************************************/




int main()
{
	//**DO NOT REMOVE THIS****
	    init_platform();
	//************************


#ifdef	enable_interrupts
	    init_interrupts();
#endif


	    //setup screen
	    setup();
	    menu_screen();


	    Xil_ExceptionEnable();



	    //Try to avoid writing any code in the main loop.
		while(1){


		}


		cleanup_platform();
		return 0;
}


//Timer interrupt handler for led matrix update. Frequency is 800 Hz
void TickHandler(void *CallBackRef){
	//Don't remove this
	uint32_t StatusEvent;

	//exceptions must be disabled when updating screen
	Xil_ExceptionDisable();



	//****Write code here ****
	// Choose the correct line and open the next one.
	closeLine();
	run(channel_pointer);
	latch();
	open_line(channel_pointer);
	// Add channel pointer one and get modulo of 8 to reset the channel pointer to make the illusion
	channel_pointer++;
	channel_pointer %= 8;


	// If the game is active, update the pxixels in the game.
	if (!game_over){
		clear_matrix();
		draw_lazer();
		draw_ship();
		draw_alien();
		move_alien();
	}



	//****END OF OWN CODE*****************

	//*********clear timer interrupt status. DO NOT REMOVE********
	StatusEvent = XTtcPs_GetInterruptStatus((XTtcPs *)CallBackRef);
	XTtcPs_ClearInterruptStatus((XTtcPs *)CallBackRef, StatusEvent);
	//*************************************************************
	//enable exceptions
	Xil_ExceptionEnable();
}


//Timer interrupt for moving alien, shooting... Frequency is 10 Hz by default
void TickHandler1(void *CallBackRef){

	//Don't remove this
	uint32_t StatusEvent;

	//****Write code here ****
	if (!game_over){
		check_lazer_hit();
		generate_alien();
		check_alien_hit();
	}


	//****END OF OWN CODE*****************
	//clear timer interrupt status. DO NOT REMOVE
	StatusEvent = XTtcPs_GetInterruptStatus((XTtcPs *)CallBackRef);
	XTtcPs_ClearInterruptStatus((XTtcPs *)CallBackRef, StatusEvent);

}


//Interrupt handler for switches and buttons.
//Reading Status will tell which button or switch was used
//Bank information is useless in this exercise
void ButtonHandler(void *CallBackRef, u32 Bank, u32 Status){
	//****Write code here ****

	//Hint: Status==0x01 ->btn0, Status==0x02->btn1, Status==0x04->btn2, Status==0x08-> btn3, Status==0x10->SW0, Status==0x20 -> SW1

	//If true, btn0 was used to trigger interrupt
	if (game_over && Status==0x08){
		game_over = 0;
		reset_variables();

	}
	// Move ship right
	else if(Status==0x01){
		if (ship_location < 7){
			ship_location++;
		}
	// Move ship left
	} else if (Status==0x04){
		if (ship_location > 0){
			ship_location--;
		}
	// Shoot lazer
	} else if (Status==0x02){
		if (lazer_y == 7){
			lazer_x = ship_location;
			lazer_y = 5;
		}
	// Assembler blinker
	}
	if (game_over && Status==0x04){
		clear_matrix();
		blinker();
	}


	//****END OF OWN CODE*****************
}

// Check if lazer hits the alien
void check_lazer_hit(){
	if (lazer_y != 7){
		if (lazer_y == 0){
			lazer_y = 7;
		} else {
			lazer_y--;
		}
	}
}

// Reset game variables
void reset_variables(){
	ship_location = 2;
	alien_x = 0;
	alien_y = 0;
	alien__move_freq_rate = 200;
	points = 0;
	lazer_x = 0;
	lazer_y = 0;
	move_freq_val = 200;
	game_over = 0;
	alien_direction = 0;
}

// Show menu screen of the game
void menu_screen(){
	 uint8_t direction = 0;
	 draw_symbols_to_matrix(text[0]);

}

void show_points(){
	uint8_t first = points / 10;
	uint8_t second = points % 10;
	uint8_t numbers[8] = {};
	for (uint8_t i= 0; i < 8; i++){
		// Concatenate number bits together to draw points to led-matrix
		uint8_t val = (text[second+1][i] << 4)| text[first+1][i];
		numbers[i] = val;
	}
	draw_symbols_to_matrix(numbers);
}

// Generate new alien if previous is destroyed
void generate_alien(){
	if (alien_y == -1){
		alien_y = 0;
		alien_x = 0;
		alien_direction = rand() % 2;
	}
}

// Check if alien is hit, add point and make the alien faster every 5 points
void check_alien_hit(){
	if (alien_x == lazer_x && alien_y == lazer_y){
		alien_y = -1;
		lazer_y = 7;
		points++;
		if (points % 5 == 0){
			move_freq_val = move_freq_val - 25;
		}
	}
}

// The software is made purposefully to skip the last x led in the row to prevent spawn camping.
void move_alien(){
	alien__move_freq_rate--;
	if (alien__move_freq_rate*10 <= 0){
		alien__move_freq_rate = move_freq_val;
		// Move alien to right direction
		if (alien_direction == 0){
			alien_x++;
			if (alien_x == 7){
				alien_y++;
				alien_direction = 1;
			}
		}
		// Move alien to left direction
		else if (alien_direction == 1) {
			alien_x--;
			if (alien_x == 0) {
				alien_y++;
				alien_direction = 0;
			}
		}
		// If alien gets to the ship -> game over.
		if (alien_y == 6){
			game_over = 1;
			ship_location = 2;
			alien_y = 0;
			alien_x = 0;
			clear_matrix();
			show_points();
			points = 0;
		}
	}
}

// Set all pixels to OFF position
void clear_matrix(){
	for (uint8_t x = 0; x <=7; x++){
		for (uint8_t y = 0; y <=7; y++){
			SetPixel(x,y,0,0,0);
		}
	}
}

// Draw ship in certain location
void draw_ship(){
	SetPixel(ship_location-1,7,255,0,0);
	SetPixel(ship_location,7,255,0,0);
	SetPixel(ship_location+1,7,255,0,0);
	SetPixel(ship_location,6,255,0,0);
}

// Draw alien in its certain location
void draw_alien(){
	if (alien_y != -1){
		SetPixel(alien_x,alien_y,0,255,0);
	}
}

// Draw lazer in its location

void draw_lazer(){
	if (lazer_y != 7){
		SetPixel(lazer_x, lazer_y,0,0,255);
	}
}

// Draw a symbol to the matrix
void draw_symbols_to_matrix(uint8_t matrix[]){
	for (uint8_t x = 0; x < 8; x++){
		uint8_t row_bits = matrix[x];
		for (uint8_t y = 8; y > 0; y--){
			if (row_bits & (1 << (y - 1))) {
				SetPixel(y-1,x,0,120,0);
			}else {
				SetPixel(y-1,x,0,0,0);
			}
			row_bits << 1;
		}
	}
}
