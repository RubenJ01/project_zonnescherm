/*
 * Leds.c
 *
 * Created: 2-11-2020 10:38:45
 *  Author: Anton Bonder2
 */ 
#include "AVR_TTC_scheduler.h"
#include "Leds.h"
#include <avr/interrupt.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/sfr_defs.h>

volatile int yellow_is_on = 0;
volatile int index_blink = 0;
volatile bool is_open = false;

void Enable_blink(){
	PORTD &= ~_BV(PORTD2);
	PORTD &= ~_BV(PORTD4);
	if (index_blink == 0){
	index_blink = SCH_Add_Task(blink,0,10);	
	}
}

void Disable_blink(){
	if(index_blink != 0){
		SCH_Delete_Task(index_blink);	
	}
	index_blink = 0;
	PORTD &= ~_BV(PORTD3);
	yellow_is_on = 0;
}

void Open(){
	PORTD |= _BV(PORTD2);
	PORTD &= ~_BV(PORTD4);
	is_open = true;
}

void Close(){
	//zonnescherm is dicht
	PORTD |= _BV(PORTD4);
	PORTD &= ~_BV(PORTD2);
	is_open = false;
}

void blink(){
	if (yellow_is_on == 1){
		PORTD &= ~_BV(PORTD3);
		yellow_is_on = 0;
	}
	else{
		PORTD |= _BV(PORTD3);
		yellow_is_on = 1;
	}
	
}