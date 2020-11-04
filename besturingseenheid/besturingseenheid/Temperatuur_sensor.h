/*
 * Temperatuur_sensor.h
 *
 * Created: 2-11-2020 11:47:38
 *  Author: Anton Bonder2
 */ 


#ifndef TEMPERATUUR_SENSOR_H_
#define TEMPERATUUR_SENSOR_H_
void Set_max_temperatuur();
void Set_min_temperatuur();
int Get_max_temperatuur();
int Get_min_temperatuur();
int Get_huidige_temperatuur();
void update_temperatuur();
#include <avr/interrupt.h>
#include <stdint.h>
#include "LDR_sensor.h"
#include <math.h>
#endif /* TEMPERATUUR_SENSOR_H_ */