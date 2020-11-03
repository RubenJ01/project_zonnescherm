/*
 * LDR_sensor.h
 *
 * Created: 2-11-2020 14:35:56
 *  Author: Anton Bonder2
 */ 

#ifndef LDR_SENSOR_H_
#define LDR_SENSOR_H_
void Set_min_lichtintensiteit();
int Get_min_lichtintensiteit();
int Get_huidige_lichtintensiteit();
void update_lichtintensiteit();
void do_conversion();

#endif /* LDR_SENSOR_H_ */