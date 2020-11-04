/*
 * Ultrasonic_sensor.h
 *
 * Created: 2-11-2020 14:38:22
 *  Author: Anton Bonder2
 */ 


#ifndef ULTRASONIC_SENSOR_H_
#define ULTRASONIC_SENSOR_H_
void update_afstand(void);
uint16_t Get_huidige_afstand(void);
void Set_max_oprol(int oprol);
void Set_min_oprol(int oprol);
int Get_max_oprol(void);
int Get_min_oprol(void);




#endif /* ULTRASONIC_SENSOR_H_ */