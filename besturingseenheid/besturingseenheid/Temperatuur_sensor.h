#ifndef TEMPERATUUR_SENSOR_H_
#define TEMPERATUUR_SENSOR_H_

#include <avr/interrupt.h>
#include <stdint.h>
#include "LDR_sensor.h"
#include <math.h>

void Set_max_temperatuur(int temperatuur);
void Set_min_temperatuur(int temperatuur);
void Set_gemiddelde_temperatuur_CB(void* callback);
int Get_max_temperatuur();
int Get_min_temperatuur();
int Get_huidige_temperatuur();
int* Get_afgelopen_gemiddelde_temperaturen();
void update_temperatuur();

#endif /* TEMPERATUUR_SENSOR_H_ */