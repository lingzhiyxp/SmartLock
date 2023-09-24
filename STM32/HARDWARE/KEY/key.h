#ifndef __KEY_H
#define __KEY_H	 
#include "sys.h"	 


#define KEY1 PAin(0)
#define KEY2 PAin(1) 
#define KEY3 PBin(12)
#define KEY4 PBin(13)
#define KEY5 PBin(14)

#define KEY1_PORT_CLK  RCC_APB2Periph_GPIOA
#define KEY1_PORT			 GPIOA
#define KEY1_PORT_PIN  GPIO_Pin_0

#define KEY2_PORT_CLK  RCC_APB2Periph_GPIOA
#define KEY2_PORT			 GPIOA
#define KEY2_PORT_PIN  GPIO_Pin_1

#define KEY3_PORT_CLK  RCC_APB2Periph_GPIOB
#define KEY3_PORT			 GPIOB
#define KEY3_PORT_PIN  GPIO_Pin_12

#define KEY4_PORT_CLK  RCC_APB2Periph_GPIOB
#define KEY4_PORT			 GPIOB
#define KEY4_PORT_PIN  GPIO_Pin_13

#define KEY5_PORT_CLK  RCC_APB2Periph_GPIOB
#define KEY5_PORT			 GPIOB
#define KEY5_PORT_PIN  GPIO_Pin_14

extern u8 key_num;

void KEY_Init(void);//IO初始化
u8 KEY_Scan(u8 mode);//按键扫描函数					    
#endif
