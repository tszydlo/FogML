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

static float Q_states[] = {-1.600000, 1.600000, 1.000000, 
-0.170000, 0.170000, 1.000000, 
-0.420000, 0.420000, 6.000000, 
-0.870000, 0.870000, 6.000000, 
};
    
unsigned int RL_OBSERVATION_SIZE = 4;

unsigned int *observation_states;

void fogml_discretizer_init(){
    
    observation_states = (float*)malloc(sizeof(unsigned int) * RL_OBSERVATION_SIZE);
}

unsigned long fogml_discretizer_get_state(float* observation){
    for(int i = 0; i < RL_OBSERVATION_SIZE; i++){
        float window = (Q_states[i*3+1] - Q_states[i*3+0]) / Q_states[i*3+2]; // (max-min) / num
        int state = (int)((observation[i] - Q_states[i*3+0]) / window) + 1;
        
        if (state < 0) {
            state = 0;
        }
        
        if (state > Q_states[i*3+2] + 1) {
            state = Q_states[i*3+2] + 1;
        }
        
        observation_states[i] = state;
    }
    
    unsigned long result = 0;
    unsigned long mul = 1;

    for(int i = 0; i < RL_OBSERVATION_SIZE; i++){
        result = result + mul * observation_states[i];
        mul = mul * (Q_states[i*3+2] + 2); 
        
    }
    
    return result;
}
