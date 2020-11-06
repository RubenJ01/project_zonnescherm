#include "Temperatuur_sensor.h"

volatile int max_temperatuur = 0;
volatile int min_temperatuur = 0;
volatile int index_seconde_array = 0;
volatile int index_gemiddelde_array = 0;
volatile int afgelopen_temperaturen[60];
volatile int afgelopen_gemiddelde_temperaturen[10];
volatile int huidige_temperatuur = 0;
volatile double temp = 0;
volatile void (*temperatuur_ptr)(int) = 0;

void Set_gemiddelde_temperatuur_CB(void* callback) {
	temperatuur_ptr = callback;
}

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

int* Get_afgelopen_gemiddelde_temperaturen() {
	return afgelopen_gemiddelde_temperaturen;
}

void update_temperatuur(){
	int i;
	ADMUX  = (1 << REFS0) | (1 << ADLAR); // Select AD0
	do_conversion();
	temp = (ADCH <<2);
	temp = temp *5;
	temp = temp/1024;
	temp = temp -0.5;
	temp = temp *100;
	if (index_seconde_array >= 59){
		int sum, loop;
		float avg;
		sum = avg = 0;
		
		for(loop = 0; loop < 59; loop++) {
			sum = sum + afgelopen_temperaturen[loop];
		}
		avg = (float)sum / loop;
		
		if (index_gemiddelde_array >= 9){
			
			for(i=10-1;i>0;i--)
			{
				afgelopen_gemiddelde_temperaturen[i]=afgelopen_gemiddelde_temperaturen[i-1];
			}
			afgelopen_gemiddelde_temperaturen[0]=round(avg);
			huidige_temperatuur=round(avg);
			
		}
		else{
			afgelopen_gemiddelde_temperaturen[index_gemiddelde_array] = round(avg);
			huidige_temperatuur=round(avg);
			index_gemiddelde_array = index_gemiddelde_array + 1;
		}
		if (temperatuur_ptr != 0) {
			temperatuur_ptr(Get_huidige_temperatuur());
		}
		
		index_seconde_array = 0;
	}
	afgelopen_temperaturen[index_seconde_array] = round(temp);
	index_seconde_array = index_seconde_array +1;
	
}