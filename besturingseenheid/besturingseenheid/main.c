#include "main.h"volatile int data_type = 0;volatile int data = 0;volatile bool automatic = false;volatile bool open = false;void uart_init()
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

uint8_t receive(void) {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

void transmit_open() {
	transmit(open);
}

void transmit_lichtintensiteit(uint8_t lichtintensiteit) {
	transmit(lichtintensiteit + 2);
}

void transmit_temperatuur(uint8_t temperatuur) {
	transmit(temperatuur + 7);
}

void transmit_all() {
	transmit(automatic); // Verstuur automatic
	transmit(open); // Verstuur of zonnescherm open of dicht is
	transmit(Get_oprol_afstand()); // Verstuur oprolafstand
	transmit(Get_uitrol_afstand()); // Verstuur uitrolafstand
	transmit(Get_min_temperatuur()); // Verstuur min temperatuur
	transmit(Get_max_temperatuur()); // Verstuur max temperatuur
	transmit(Get_min_lichtintensiteit()); // Verstuur min lichtintensiteit
	// Verstuur de afgelopen 10 gemiddelde temperaturen
	int* gemiddelde_temperaturen = Get_afgelopen_gemiddelde_temperaturen();
	for (int i = 0; i < 10; ++i) {		transmit(gemiddelde_temperaturen[i]);	}
	// Verstuur de afgelopen 10 gemiddelde lichtintensiteiten
	int* gemiddelde_lichtintensiteiten = Get_afgelopen_gemiddelde_lichtintensiteiten();
	for (int i = 0; i < 10; ++i) {
		transmit(gemiddelde_lichtintensiteiten[i]);	
	}
	transmit(Get_temperatuur_counter());
	transmit(Get_lichtintensiteit_counter());
}

void verwerk_data(){
	if (data_type == 0) {
		// Verzoek om alle instellingen op te sturen
		if (data == 1) {
			transmit_all();
			return;
		}
		data_type = data;
	}
	else {
		switch (data_type){
			case 2: // Set automatic
				automatic = data ? true : false;
				break;
			case 3: // Open of sluit zonnescherm
				if (open == true)	{ open = false; Close(); }
				else				{ open = true; Open(); }
				break;
			case 4: // Set oprol_afstand
				Set_oprol_afstand(data);
				break;
			case 5: // Set uitrol_afstand
				Set_uitrol_afstand(data);
				break;
			case 6: // Set min_temperatuur
				Set_min_temperatuur(data);
				break;
			case 7: // Set max_temperatuur
				Set_max_temperatuur(data);
				break;
			case 8: // Set min_lichtintensiteit
				Set_min_lichtintensiteit(data);
				break;
		}
		data_type = 0;
	}
	/*if (data == 0b00000001){
		Enable_blink();
	}
	else if (data == 0b00000010){
		Disable_blink();
	}*/
}

void Update_main() {
	// Als automatic aanstaat moet er gecheckt worden of de temperatuur en lichtintensiteit tussen een bepaalde waarde valt. 
	// Als dat zo is moet het zonnescherm open gaan, mits die niet al open is.
	if (automatic == true) {
		int temperatuur = Get_huidige_temperatuur();
		int lichtintesiteit = Get_huidige_lichtintensiteit();
		if ((Get_min_temperatuur() <= temperatuur && Get_max_temperatuur() >= temperatuur) || Get_min_lichtintensiteit() <= lichtintesiteit) {
			open = true;
		}
		else {
			open = false;
		}
		// Als open is verandert door de automatic roepen we transmit_open() aan
		if (open != Is_open()) {
			transmit_open();
		}
	}
	// Check of de status van het zonnescherm is verandert, zo ja dan sluiten we of openen we het zonnescherm
	if (open != Is_open()) {
		if (open) { 
			Open();
		}
		else {
			Close();
		}
	}
	// Check of het zonnescherm volledig is opgerold of uitgerold, als dat niet het geval is dan laten we de gele led knipperen
	int afstand = Get_huidige_afstand();
	if (open) {
		// Doe blink uit als de uitrol_afstand lager is dan de afstand
		if (Get_uitrol_afstand() <= afstand) {
			if (Is_blinking()) { Disable_blink(); }
		}
		// Doe blink aan als de uitrol_afstand groter is dan de afstand
		else {
			if (!Is_blinking()) { Enable_blink(); }
		}
	}
	else {
		// Doe blink uit als de oprol_afstand groter is dan de afstand
		if (Get_oprol_afstand() >= afstand) {
			if (Is_blinking()) { Disable_blink(); }
		} // Doe blink aan als de oprol_afstand kleiner is dan de afstand
		else {
			if (!Is_blinking()) { Enable_blink(); }
		}
	}
}

int main(void)
{
	// Intialiseer alles
	init();
	uart_init();	init_adc();	
	// Close zonnescherm standaard zodat het rode lode lampje brandt
	Close();
	
	// Deze twee callbacks zorgen ervoor dat wanneer er een nieuwe gemiddelde temperatuur of lichtintensiteit binnenkomt dat die automatisch verstuurd wordt naar de python applicatie
	Set_gemiddelde_lichtintensiteit_CB(transmit_lichtintensiteit);
	Set_gemiddelde_temperatuur_CB(transmit_temperatuur);
	
	//tasken toevoegen
	SCH_Add_Task(update_afstand,0,50); // Update elke 0.5 seconden
	SCH_Add_Task(update_lichtintensiteit,0,100); // Update elke 1.0 seconden
	SCH_Add_Task(update_temperatuur,0,100); // Update elke 1.0 seconden
	SCH_Add_Task(Update_main,0,100); // Update elke 1.0 seconden
	_delay_ms(2000); 
	
	while (1) 
    {	
		//check of er data binnen is
		if (UCSR0A & (1<<RXC0)){
			data = receive();
			verwerk_data();
		}
		// Dispatch tasks
		SCH_Dispatch_Tasks();
		
    }
}

