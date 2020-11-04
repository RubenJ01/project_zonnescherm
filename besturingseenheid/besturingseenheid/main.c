/*
 * besturingseenheid.c
 *
 * Created: 2-11-2020 10:05:32
 * Author : Anton Bonder2
 */ 

#include "main.h"volatile int data;volatile bool automatic = false;void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter
	//UCSR0B = _BV(TXEN0);
	UCSR0B = (1 << TXEN0) | (1 << RXEN0);
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
}uint8_t receive(void) {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}

void init(){
	DDRD |= _BV(DDD2);
	DDRD |= _BV(DDD3);
	DDRD |= _BV(DDD4);
	DDRD |= _BV(DDD5);
	
	//timer
	SCH_Init_T1();
	SCH_Start();
}

void verwerk_data(){
	if (data == 0b00000001){
		Enable_blink();
	}
	else if (data == 0b00000010){
		Disable_blink();
	}
}

int main(void)
{
	init();
	uart_init();	init_adc();	
	//tasken toevoegen
	SCH_Add_Task(update_afstand,0,50);
	SCH_Add_Task(update_lichtintensiteit,0,100);
	SCH_Add_Task(update_temperatuur,0,100);
	_delay_ms(2000); 
	
	while (1) 
    {	
		//transmit(Get_huidige_lichtintensiteit()); _delay_ms(1000);
		//transmit(Get_huidige_temperatuur()); _delay_ms(1000);
		//transmit(Get_huidige_afstand()); _delay_ms(1000);
		
		//check of data binnen is
		if (UCSR0A & (1<<RXC0)){
			data = receive();
			verwerk_data();
		}
		SCH_Dispatch_Tasks();
		
    }
}

