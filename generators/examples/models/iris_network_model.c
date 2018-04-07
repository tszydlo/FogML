#include <Arduino.h>
#include "neural_nets.h"
const float pmdata_00[] PROGMEM = {-0.482009, -0.280405, -0.177204, 0.454541, };
const float pmdata_01[] PROGMEM = {0.281752, -0.240362, 0.384827, -0.657338, };
const float pmdata_02[] PROGMEM = {-0.408962, -0.516171, -0.164047, 0.422353, };
const float pmdata_03[] PROGMEM = {0.373066, 0.401159, -0.363002, -0.397834, };
const float pmdata_04[] PROGMEM = {-0.515531, 0.358335, 0.160756, -0.011017, };
const float pmdata_05[] PROGMEM = {0.470599, 0.000930, -0.152029, -0.476776, };
const float pmdata_06[] PROGMEM = {-0.030902, 0.489950, 0.158440, -0.396958, };
const float pmdata_07[] PROGMEM = {-0.256793, 0.339329, -0.093367, -0.008804, };
const float pmdata_10[] PROGMEM = {-0.091420, -0.372177, 0.091856, 0.244726, 0.017972, -0.532419, -0.253732, 0.109035, };
const float pmdata_11[] PROGMEM = {-0.410996, -0.282101, -0.252966, -0.870360, -0.353737, 0.236617, 0.395521, 0.330120, };
const float pmdata_12[] PROGMEM = {0.543101, 0.193929, 0.287204, -0.900307, -0.229414, 0.413531, -0.772979, -0.174224, };
int evaluate_network(uint8_t * x){
 float result0[8];
result0[0]=0;
for(int i=0;i<4;i++){result0[0]+=(float)pgm_read_float_near(pmdata_00+i) * (float)x[i];}
result0[1]=0;
for(int i=0;i<4;i++){result0[1]+=(float)pgm_read_float_near(pmdata_01+i) * (float)x[i];}
result0[2]=0;
for(int i=0;i<4;i++){result0[2]+=(float)pgm_read_float_near(pmdata_02+i) * (float)x[i];}
result0[3]=0;
for(int i=0;i<4;i++){result0[3]+=(float)pgm_read_float_near(pmdata_03+i) * (float)x[i];}
result0[4]=0;
for(int i=0;i<4;i++){result0[4]+=(float)pgm_read_float_near(pmdata_04+i) * (float)x[i];}
result0[5]=0;
for(int i=0;i<4;i++){result0[5]+=(float)pgm_read_float_near(pmdata_05+i) * (float)x[i];}
result0[6]=0;
for(int i=0;i<4;i++){result0[6]+=(float)pgm_read_float_near(pmdata_06+i) * (float)x[i];}
result0[7]=0;
for(int i=0;i<4;i++){result0[7]+=(float)pgm_read_float_near(pmdata_07+i) * (float)x[i];}
result0[0] = result0[0] + (0.555641);
result0[1] = result0[1] + (0.479223);
result0[2] = result0[2] + (0.475145);
result0[3] = result0[3] + (0.188473);
result0[4] = result0[4] + (0.453912);
result0[5] = result0[5] + (0.463577);
result0[6] = result0[6] + (0.492588);
result0[7] = result0[7] + (-0.066003);
for (int i=0; i < 8; i++){ if (result0[i] < 0) { result0[i] = 0;}}
float result1[3];
result1[0]=0;
for(int i=0;i<8;i++){result1[0]+=(float)pgm_read_float_near(pmdata_10+i) * (float)result0[i];}
result1[1]=0;
for(int i=0;i<8;i++){result1[1]+=(float)pgm_read_float_near(pmdata_11+i) * (float)result0[i];}
result1[2]=0;
for(int i=0;i<8;i++){result1[2]+=(float)pgm_read_float_near(pmdata_12+i) * (float)result0[i];}
result1[0] = result1[0] + (0.135601);
result1[1] = result1[1] + (-0.478698);
result1[2] = result1[2] + (0.547264);
double max_el = result1[0];for (int i=1; i < 3; i++){max_el = max(max_el, result1[i]);}double exp_sum = 0.0; 
for (int i=0; i<3; i++){ exp_sum += exp(result1[i]-max_el); } 
for (int i=0; i<3; i++){ result1[i] = exp(result1[i]-max_el) / exp_sum; }
int max_index = 0;
for (int i = 0; i < 3; i++){ if (result1[i] > result1[max_index]){ max_index = i; }}
return max_index;

 }; 
 