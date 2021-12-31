#include <Arduino.h>
#include "neural_nets.h"
const float pmdata_00[] PROGMEM = {-0.035431, -0.046410, -0.002355, 0.009097, };
const float pmdata_01[] PROGMEM = {0.387625, 0.601107, -0.278682, -0.069962, };
const float pmdata_02[] PROGMEM = {-0.017275, -0.000000, -0.046636, 0.002225, };
const float pmdata_03[] PROGMEM = {0.233183, -0.519569, 0.625201, 1.157216, };
const float pmdata_10[] PROGMEM = {0.000109, 0.558352, 0.029461, -2.040082, };
const float pmdata_11[] PROGMEM = {0.000000, 0.366993, -0.008656, -0.624923, };
const float pmdata_12[] PROGMEM = {-0.000000, -0.875632, 0.000000, 0.348823, };
int evaluate_network(uint8_t * x){
 float result0[4];
result0[0]=0;
for(int i=0;i<4;i++){result0[0]+=(float)pgm_read_float_near(pmdata_00+i) * (float)x[i];}
result0[1]=0;
for(int i=0;i<4;i++){result0[1]+=(float)pgm_read_float_near(pmdata_01+i) * (float)x[i];}
result0[2]=0;
for(int i=0;i<4;i++){result0[2]+=(float)pgm_read_float_near(pmdata_02+i) * (float)x[i];}
result0[3]=0;
for(int i=0;i<4;i++){result0[3]+=(float)pgm_read_float_near(pmdata_03+i) * (float)x[i];}
result0[0] = result0[0] + (-0.395456);
result0[1] = result0[1] + (0.519410);
result0[2] = result0[2] + (-0.376649);
result0[3] = result0[3] + (-0.785912);
for (int i=0; i < 4; i++){ if (result0[i] < 0) { result0[i] = 0;}}
float result1[3];
result1[0]=0;
for(int i=0;i<4;i++){result1[0]+=(float)pgm_read_float_near(pmdata_10+i) * (float)result0[i];}
result1[1]=0;
for(int i=0;i<4;i++){result1[1]+=(float)pgm_read_float_near(pmdata_11+i) * (float)result0[i];}
result1[2]=0;
for(int i=0;i<4;i++){result1[2]+=(float)pgm_read_float_near(pmdata_12+i) * (float)result0[i];}
result1[0] = result1[0] + (1.563457);
result1[1] = result1[1] + (0.325254);
result1[2] = result1[2] + (0.414821);
double max_el = result1[0];for (int i=1; i < 3; i++){max_el = max(max_el, result1[i]);}double exp_sum = 0.0; 
for (int i=0; i<3; i++){ exp_sum += exp(result1[i]-max_el); } 
for (int i=0; i<3; i++){ result1[i] = exp(result1[i]-max_el) / exp_sum; }
int max_index = 0;
for (int i = 0; i < 3; i++){ if (result1[i] > result1[max_index]){ max_index = i; }}
return max_index;

 }; 
 