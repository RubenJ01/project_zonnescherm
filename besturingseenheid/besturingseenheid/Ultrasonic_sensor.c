/*
 * Ultrasonic_sensor.c
 *
 * Created: 2-11-2020 14:37:41
 *  Author: Anton Bonder2
 */ 
#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "distance.h"

volatile uint16_t gv_counter; // 16 bit counter value
volatile uint16_t huidige_afstand;
volatile uint8_t min_oprol_afstand = 10;
volatile uint8_t max_oprol_afstand = 50;

uint16_t calc_cm(uint16_t counter)
{
	// counter 0 ... 65535, f = 16 MHz
	uint16_t micro_sec = counter;
	// micro_sec: 0..4095 cm: 0..70 (so 70 cm is max)
	return ((micro_sec / 58.2) *2);
	//return ((micro_sec*0.034)*2);
}

void update_afstand(void){
	// start trigger pulse lo -> hi (D0)
	PORTD |= _BV(5);
	_delay_us(12); // micro sec
	//_delay_us(1200000); //test
	// stop trigger pulse hi -> lo (D0)
	//PORTD = 0x00;
	PORTD &= ~_BV(5);
	gv_counter = 0;
	
	while ((PIND & 0b01000000) != 0b01000000){
	}
	while((PIND & 0b01000000) == 0b01000000){
	_delay_us(1);	
	gv_counter = gv_counter + 1;
	}
	_delay_ms(30);
	// wait 30 milli sec, gv_counter == timer1 (read in ISR)
	
	//huidige_afstand = 20;
	huidige_afstand = calc_cm(gv_counter);
	//huidige_afstand = gv_counter;
}

uint16_t Get_huidige_afstand(){
	return huidige_afstand;
}

void Set_max_oprol(int oprol){
	max_oprol_afstand = oprol;
}

void Set_min_oprol(int oprol){
	min_oprol_afstand = oprol;
}

int Get_max_oprol(void){
	return max_oprol_afstand;
}

int Get_min_oprol(void){
	return min_oprol_afstand;
}