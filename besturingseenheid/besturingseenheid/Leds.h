#ifndef LEDS_H_
#define LEDS_H_

#include "AVR_TTC_scheduler.h"
#include <avr/interrupt.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/sfr_defs.h>

int Is_blinking();
void Enable_blink();
void Disable_blink();
bool Is_open();
void Open();
void Close();
void blink();

#endif /* LEDS_H_ */