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

#ifndef FOGML_RL_H
#define FOGML_RL_H

#ifdef __cplusplus
extern "C" {
#endif

void fogml_qlearning_init();
void fogml_qlearning_update_state(unsigned long state);
unsigned int fogml_qlearning_select_action();

void fogml_discretizer_init();
unsigned long fogml_discretizer_get_state(float* observation);

extern unsigned long RL_STATES;
extern unsigned int  RL_ACTIONS;
extern unsigned int RL_OBSERVATION_SIZE;

#ifdef __cplusplus
}
#endif

#endif


