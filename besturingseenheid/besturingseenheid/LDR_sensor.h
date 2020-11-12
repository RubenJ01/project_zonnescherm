#ifndef LDR_SENSOR_H_
#define LDR_SENSOR_H_

#include <avr/interrupt.h>
#include <stdint.h>
#include <math.h>

void Set_min_lichtintensiteit(int lichtintensiteit);
void Set_gemiddelde_lichtintensiteit_CB(void* callback);
int Get_min_lichtintensiteit();
int Get_huidige_lichtintensiteit();
int* Get_afgelopen_gemiddelde_lichtintensiteiten();
int Get_lichtintensiteit_counter();
void update_lichtintensiteit();
void do_conversion();

#endif /* LDR_SENSOR_H_ */