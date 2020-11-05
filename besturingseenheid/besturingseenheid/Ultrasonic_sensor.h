#ifndef ULTRASONIC_SENSOR_H_
#define ULTRASONIC_SENSOR_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "distance.h"

uint16_t calc_cm(uint16_t counter);
void update_afstand(void);
uint16_t Get_huidige_afstand(void);
void Set_uitrol_afstand(uint8_t uitrol);
void Set_oprol_afstand(uint8_t oprol);
uint8_t Get_uitrol_afstand(void);
uint8_t Get_oprol_afstand(void);

#endif /* ULTRASONIC_SENSOR_H_ */