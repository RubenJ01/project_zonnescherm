/*
 * LDR_sensor.c
 *
 * Created: 2-11-2020 14:34:21
 *  Author: Anton Bonder2
 */ 
#include <avr/interrupt.h>
#include <stdint.h>

volatile int min_lichtintensiteit = 0;
volatile int huidige_lichtintensiteit = 0;

void Set_min_lichtintensiteit(int lichtintensiteit){
	min_lichtintensiteit = lichtintensiteit;
}

int Get_min_lichtintensiteit(){
	return min_lichtintensiteit;
}

int Get_huidige_lichtintensiteit(){
	return huidige_lichtintensiteit;
}

void do_conversion()
{
	ADCSRA |= (1 << ADSC);   // Start conversie

	// Wacht tot conversie klaar (ADIF)
	while ((ADCSRA & (1 << ADIF)) == 0)
	{
		// Doe niets.
	}
}

void update_lichtintensiteit(){
	//nieuw 2.0
	ADMUX  = (1 << REFS0) | (1 << ADLAR) | (1 << MUX0); // Select AD1
	do_conversion();
	huidige_lichtintensiteit = (ADCH <<2);
	
	
	
	
	//do_conversion();
	//ADMUX  = (0b01 << REFS0) | ( 0b001 << MUX0) | (1 << ADLAR); // Select AD1
	//ADCSRA |= (1<<ADSC);   // Start conversie
	// Wacht tot conversie klaar (ADIF)
	//while ((ADCSRA & (1 << ADIF)) == 0);
	//loop_until_bit_is_clear(ADCSRA, ADSC);
	//huidige_lichtintensiteit = (ADCH <<2);
	//return (ADCH <<2) ;//+ ADCL; // 8-bit resolution, left adjusted
}