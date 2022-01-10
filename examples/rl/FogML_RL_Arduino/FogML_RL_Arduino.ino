/*
   Copyright 2021 FogML

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include "fogml_rl.h"

float *observations;
unsigned long state;
unsigned int action;

// For Arduino Nano BLE 33
#define LED 22

int led_state;

void toggle_led(){
  digitalWrite(LED, led_state);
  led_state = 1 - led_state;
}

void setup() {
  //initialize serial:
  Serial.begin(115200);

  pinMode(LED, OUTPUT);
  led_state = 0;

  //states = (float*)malloc(sizeof(float) * RL_STATES);
  observations = (float*)malloc(sizeof(float) * RL_STATES);

  fogml_qlearning_init();
  fogml_discretizer_init();
}

void loop() {
  toggle_led();
  
  while (Serial.available() > 0) {

    char c;
    for(int i = 0; i < RL_OBSERVATION_SIZE; i++){
      float obs = Serial.parseFloat(SKIP_NONE);
      observations[i]=obs;

      //read delimiter or new line
      c = Serial.read();
    }

    //after last float should be a new line
    if (c == '\n' || c == '\r') {
      
      if (Serial.peek() == '\n'){
        Serial.read();
      }
      
      //RL Discretize Observations
      state = fogml_discretizer_get_state(observations);
      //RL Update State
      fogml_qlearning_update_state(state);
      //RL Select Action
      action = fogml_qlearning_select_action();
      
      Serial.println(action);
    } else {
      Serial.println("ERROR");
    }
  }
}
