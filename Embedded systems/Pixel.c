/*
 * Pixel.c
 *
 *  Created on: -----
 *      Author: -----
 */

#include "Pixel.h"


//Table for pixel dots.
//				 dots[X][Y][COLOR]
volatile uint8_t dots[8][8][3]={0};

// Define pointers to memory addresses
#define control_ptr (uint8_t *) 0x41220008
#define channel_ptr (uint8_t *) 0x41220000

// Here the setup operations for the LED matrix will be performed
void setup(){

	//reseting screen at start is a MUST to operation (Set RST-pin to 1).
	*control_ptr = 0;
	*channel_ptr = 0;

	// Toggle RST bit
	*control_ptr |= 1;
	usleep(500);

	*control_ptr &= 0;
	usleep(500);

	*control_ptr |= 1;
	usleep(500);

	// Set sda bit
	*control_ptr |= 0x10;
	*control_ptr|=0x08;
	//Write code that sets 6-bit values in register of DM163 chip. Recommended that every bit in that register is set to 1. 6-bits and 24 "bytes", so some kind of loop structure could be nice.
	//24*6 bits needs to be transmitted
	// Create the RGB brightness vector
	uint8_t brigtness[] = {63, 63, 63};
	for(uint8_t led = 0; led <= 7; led++){
		for(uint8_t rgb = 0; rgb <=2; rgb++){
			uint8_t led_color = brigtness[rgb];
			for(uint8_t bit_index = 0; bit_index <= 5; bit_index++){
				if(led_color & 0b100000){
					*control_ptr |= 0x10;
				} else {
					*control_ptr &=~0x10;
				}
				*control_ptr&=~0x08;
				led_color <<=1;
				*control_ptr|=0x08;
			}

		}
	}


	//Final thing in this function is to set SB-bit to 1 to enable transmission to 8-bit register.
	*control_ptr |= 0b100;

}

//Change value of one pixel at led matrix. This function is only used for changing values of dots array
void SetPixel(uint8_t x,uint8_t y, uint8_t r, uint8_t g, uint8_t b){

	//Hint: you can invert Y-axis quite easily with 7-y
	dots[x][y][0]=b;
	//Write rest of two lines of code required to make this function work properly (green and red colors to array).
	dots[x][y][1]=g;
	dots[x][y][2]=r;

}


//Put new data to led matrix. Hint: This function is supposed to send 24-bytes and parameter x is for channel x-coordinate.
void run(uint8_t x){



	//Write code that writes data to led matrix driver (8-bit data). Use values from dots array
	//Hint: use nested loops (loops inside loops)
	//Hint2: loop iterations are 8,3,8 (pixels,color,8-bitdata)
	latch();
	for(uint8_t y=0; y<8; y++){
		for(uint8_t color=0; color<3; color++){
			// Read dots array to some temporally variable. This variable is used in sending data
			uint8_t led_data = dots[x][y][color];
			for(uint8_t byte_count=0; byte_count<8; byte_count++){
				if(led_data & 0x80){
					*control_ptr|=0x10;
				}else{
					*control_ptr&=~0x10;
				}
				*control_ptr&=~0x08;
				led_data <<=1;
				*control_ptr |= 0x08;

			}
		}
	}
	latch();

}

//Latch signal. See colorsshield.pdf or DM163.pdf in project folder on how latching works
void latch(){
	*control_ptr |= 0b10;
	*control_ptr &=~0b10;

}


//Set one line (channel) as active, one at a time.
void open_line(uint8_t x){
	switch(x){
		case 0b0: *channel_ptr = 0x01 ; break;
		case 0b1: *channel_ptr = 0x02; break;
		case 0b10: *channel_ptr = 0x04; break;
		case 0b11: *channel_ptr = 0x08; break;
		case 0b100: *channel_ptr = 0x10; break;
		case 0b101: *channel_ptr = 0x20; break;
		case 0b110: *channel_ptr = 0x40; break;
		case 0b111: *channel_ptr = 0x80; break;
		default: *channel_ptr=0;
	}

}

// Set all channels 0
void closeLine() {
	*channel_ptr = 0;
}



