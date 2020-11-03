/*
 * besturingseenheid.c
 *
 * Created: 2-11-2020 10:05:32
 * Author : Anton Bonder2
 */ 

#include <avr/io.h>
#include <avr/sfr_defs.h>
#include "Leds.h"
#include "AVR_TTC_scheduler.h"
#include "LDR_sensor.h"
#include "Temperatuur_sensor.h"
#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>#define UBBRVAL 51void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter
	UCSR0B = _BV(TXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}void init_adc()
{
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

void init(){
	DDRD |= _BV(DDD2);
	DDRD |= _BV(DDD3);
	DDRD |= _BV(DDD4);
	
	//timer
	SCH_Init_T1();
	SCH_Start();
	
}

int main(void)
{
	init();
	uart_init();	init_adc();	_delay_ms(1000);
    /* Replace with your application code */
	//Enable_blink();
	//Disable_blink();
    //Open();
	//Close();
	//test = Get_max_temperatuur();
	SCH_Add_Task(update_lichtintensiteit,0,25);
	SCH_Add_Task(update_temperatuur,0,25);
	
	while (1) 
    {	
		transmit(Get_huidige_lichtintensiteit()); _delay_ms(1000);
		transmit(Get_huidige_temperatuur()); _delay_ms(1000);
		SCH_Dispatch_Tasks();
    }
}

