#include "LDR_sensor.h"

volatile int min_lichtintensiteit = 0;
volatile int afgelopen_lichtintensiteiten[60];
volatile int afgelopen_gemiddelde_lichtintensiteiten[10];
volatile int huidige_lichtintensiteit = 0;
volatile int index_seconde_array_lichtintensiteiten = 0;
volatile int index_seconde_array_lichtintensiteiten_gemiddeld = 0;
volatile void (*lichtintensiteit_ptr)(int) = 0;

void Set_min_lichtintensiteit(int lichtintensiteit){
	min_lichtintensiteit = lichtintensiteit;
}

void Set_gemiddelde_lichtintensiteit_CB(void* callback) {
	lichtintensiteit_ptr = callback;
}

int Get_min_lichtintensiteit(){
	return min_lichtintensiteit;
}

int Get_huidige_lichtintensiteit(){
	return huidige_lichtintensiteit;
}

int* Get_afgelopen_gemiddelde_lichtintensiteiten() {
	return afgelopen_gemiddelde_lichtintensiteiten;
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
	ADMUX  = (1 << REFS0) | (1 << ADLAR) | (1 << MUX0); // Select AD1
	do_conversion();
	
	int i;
	
	
	//huidige_lichtintensiteit = (ADCH <<2);
	int huidige_lichtintensiteit = (ADCH);
	switch (huidige_lichtintensiteit){
		case 0 ... 40:
			huidige_lichtintensiteit = 0; 
			break;
		case 41 ... 90:
			huidige_lichtintensiteit = 1;
			break;
		case 91 ... 150:
			huidige_lichtintensiteit = 2;
			break;
		case 151 ... 220:
			huidige_lichtintensiteit = 3;
			break;
		case 221 ... 255:
			huidige_lichtintensiteit = 4;
			break;
	}
	if (index_seconde_array_lichtintensiteiten >= 59){
		int sum, loop;
		float avg;
		sum = avg = 0;
		
		for(loop = 0; loop < 59; loop++) {
			sum = sum + afgelopen_lichtintensiteiten[loop];
		}
		avg = (float)sum / loop;
		
		if (index_seconde_array_lichtintensiteiten_gemiddeld >= 9){
			
			for(i=10-1;i>0;i--)
			{
				afgelopen_gemiddelde_lichtintensiteiten[i]=afgelopen_gemiddelde_lichtintensiteiten[i-1];
			}
			afgelopen_gemiddelde_lichtintensiteiten[0]=round(avg);
			huidige_lichtintensiteit=round(avg);
			
		}
		else{
			afgelopen_gemiddelde_lichtintensiteiten[index_seconde_array_lichtintensiteiten_gemiddeld] = round(avg);
			huidige_lichtintensiteit=round(avg);
			index_seconde_array_lichtintensiteiten_gemiddeld = index_seconde_array_lichtintensiteiten_gemiddeld + 1;
		}
		if (lichtintensiteit_ptr != 0) {
			lichtintensiteit_ptr(Get_huidige_lichtintensiteit());
		}
		
		index_seconde_array_lichtintensiteiten = 0;
	}
	afgelopen_lichtintensiteiten[index_seconde_array_lichtintensiteiten] = huidige_lichtintensiteit;
	index_seconde_array_lichtintensiteiten = index_seconde_array_lichtintensiteiten +1;
	
	
}