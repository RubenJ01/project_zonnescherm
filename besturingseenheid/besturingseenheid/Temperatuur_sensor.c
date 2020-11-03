/*
 * Temperatuur_sensor.c
 *
 * Created: 2-11-2020 11:47:14
 *  Author: Anton Bonder2
 */ 

#include <avr/interrupt.h>
#include <stdint.h>
#include "LDR_sensor.h"

volatile int max_temperatuur = 0;
volatile int min_temperatuur = 0;
volatile int huidige_temperatuur = 0;
volatile double temp = 0;



void Set_max_temperatuur(int temperatuur){
	max_temperatuur = temperatuur;
}

void Set_min_temperatuur(int temperatuur){
	min_temperatuur = temperatuur;
}

int Get_max_temperatuur(){
	return max_temperatuur;
}

int Get_min_temperatuur(){
	return min_temperatuur;
}

int Get_huidige_temperatuur(){
	return huidige_temperatuur;
}

void update_temperatuur(){
	//oud
	//ADCSRA |= (1<<ADSC); // start conversion
	//loop_until_bit_is_clear(ADCSRA, ADSC);
	//nieuw
	
	//ADMUX  = (0b01 << REFS0) | ( 0b000 << MUX0) | (1 << ADLAR); // Select AD0
	//ADCSRA |= (1<<ADSC);   // Start conversie
    // Wacht tot conversie klaar (ADIF)
    //while ((ADCSRA & (1 << ADIF)) == 0);
	
	//nieuw test 2.000
	ADMUX  = (1 << REFS0) | (1 << ADLAR); // Select AD0
	do_conversion();
	
	//loop_until_bit_is_clear(ADCSRA, ADSC);

	temp = (ADCH <<2);
	temp = temp *5;
	temp = temp/1024;
	temp = temp -0.5;
	temp = temp *100;
	huidige_temperatuur = (int) temp;
	//return (ADCH <<2) ;//+ ADCL; // 8-bit resolution, left adjusted
}