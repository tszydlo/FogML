#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include "neural_nets.h"
#include "tree.h"
//#include "bayes_model.h"

MCUFRIEND_kbv tft;       // hard-wired for UNO shields anyway.

// most mcufriend shields use these pins and Portrait mode:
uint8_t YP = A2;  // must be an analog pin, use "An" notation!
uint8_t XM = A3;  // must be an analog pin, use "An" notation!
uint8_t YM = 8;   // can be a digital pin
uint8_t XP = 9;   // can be a digital pin
uint8_t SwapXY = 0;

// For better pressure precision, we need to know the resistance
// between X+ and X- Use any multimeter to read it
// For the one we're using, its 300 ohms across the X plate
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);
TSPoint tp;

#define MINPRESSURE 20
#define MAXPRESSURE 1000

#define SWAP(a, b) {uint16_t tmp = a; a = b; b = tmp;}


uint8_t char_buff[28*28];

int16_t BOXSIZE;
int16_t PENRADIUS = 3;
uint16_t identifier, oldcolor, currentcolor;
uint8_t Orientation = 1;    //PORTRAIT

// Assign human-readable names to some common 16-bit color values:
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

uint16_t TS_LEFT = 920;
uint16_t TS_RT  = 150;
uint16_t TS_TOP = 940;
uint16_t TS_BOT = 120;

uint16_t points=0;

uint16_t convertRGB( uint8_t R, uint8_t G, uint8_t B)
{
  return ( ((R & 0xF8) << 8) | ((G & 0xFC) << 3) | (B >> 3) );
}

uint16_t convertGREY( uint8_t v)
{
  return convertRGB(v,v,v);
}


uint16_t scale_img(uint8_t x, uint8_t y){
  return y*28 + x;
}


void copy_img(uint8_t* src, uint8_t* dst){
  int tmp;
  for(tmp=0; tmp<28*28; tmp++){
    dst[tmp]=src[tmp];
  }
}

void img_move_to_corner(){
  uint8_t buff_tmp[28*28];
  uint8_t min_x, min_y, color;

  min_x=28;
  min_y=28;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      color = char_buff[scale_img(x, y)];

      if (color==255){
        min_x = min(min_x, x);
        min_y = min(min_y, y);
      }
    }
  }

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
      if (x+min_x >=28 || y+min_y >=28) continue;
      buff_tmp[scale_img(x, y)] = char_buff[scale_img(x+min_x, y+min_y)];
    }
  }

  copy_img(buff_tmp, char_buff);
}

void img_scale_from_corner(){
  uint8_t buff_tmp[28*28];
  uint8_t max_x, max_y, color;

  max_x=0;
  max_y=0;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      color = char_buff[scale_img(x, y)];

      if (color==255){
        max_x = max(max_x, x);
        max_y = max(max_y, y);
      }
    }
  }

  float sx = 19.0/max_x;
  float sy = 19.0/max_y;

  float ss = min(sx,sy);

  Serial.println("SCALING FACTOR " + String(ss));

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
      if (x/ss >=28 || y/ss >=28) continue;
      buff_tmp[scale_img(x, y)] = char_buff[scale_img(x/ss, y/ss)];
    }
  }

  copy_img(buff_tmp, char_buff);
}


void img_center(){
  uint8_t buff_tmp[28*28];
  uint8_t max_x, max_y, color;
  uint8_t d_x, d_y;
  max_x=0;
  max_y=0;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      color = char_buff[scale_img(x, y)];

      if (color==255){
        max_x = max(max_x, x);
        max_y = max(max_y, y);
      }
    }
  }

  Serial.println("CENTERING " + String(max_x) + " , " + String(max_y));

  d_x = (28-max_x)/2;
  d_y = (28-max_y)/2;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
      if (x-d_x < 0 || y-d_y < 0) continue;
      
      buff_tmp[scale_img(x, y)] = char_buff[scale_img(x-d_x, y-d_y)];
    }
  }

  copy_img(buff_tmp, char_buff);
}

void img_weighted_center(){
  uint8_t buff_tmp[28*28];
  uint8_t d_x, d_y;

  float sum_x, sum_y, sum_w,w;
  sum_x=0;
  sum_y=0;
  sum_w=0;
  
  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      w= float(char_buff[scale_img(x, y)])/255.0;
      sum_x+=w*x;
      sum_y+=w*y;
      sum_w+=w;
    }
  }

  d_x = 14-sum_x/sum_w;
  d_y = 14-sum_y/sum_w;

  Serial.println("WEIGHTED CENTERING " + String(d_x) + " , " + String(d_y));


  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
      if (x-d_x < 0 || y-d_y < 0) continue;
      
      buff_tmp[scale_img(x, y)] = char_buff[scale_img(x-d_x, y-d_y)];
    }
  }

  copy_img(buff_tmp, char_buff);
}


void img_blur(){
  uint8_t buff_tmp[28*28];
  uint16_t tmp;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
    }
  }
 
  for(uint8_t x=1; x<27; x++){
    for(uint8_t y=1; y<27; y++){
      buff_tmp[scale_img(x, y)] = 0;

      tmp=0;

      tmp += char_buff[scale_img(x, y)];
      tmp += char_buff[scale_img(x-1, y)];
      tmp += char_buff[scale_img(x-1, y-1)];
      tmp += char_buff[scale_img(x, y-1)];
      tmp += char_buff[scale_img(x+1, y-1)];
      tmp += char_buff[scale_img(x+1, y)];
      tmp += char_buff[scale_img(x+1, y+1)];
      tmp += char_buff[scale_img(x, y+1)];
      tmp += char_buff[scale_img(x-1, y+1)];
      
      buff_tmp[scale_img(x, y)] = tmp/9;
    }
  }
}

void img_smooth(){
  uint8_t buff_tmp[28*28];
  uint16_t tmp;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      buff_tmp[scale_img(x, y)] = 0;
    }
  }
 
  for(uint8_t x=1; x<27; x++){
    for(uint8_t y=1; y<27; y++){
      buff_tmp[scale_img(x, y)] = 0;

      tmp=0;

      //tmp += char_buff[scale_img(x, y)];
      tmp += char_buff[scale_img(x-1, y)];
      tmp += char_buff[scale_img(x-1, y-1)];
      tmp += char_buff[scale_img(x, y-1)];
      tmp += char_buff[scale_img(x+1, y-1)];
      tmp += char_buff[scale_img(x+1, y)];
      tmp += char_buff[scale_img(x+1, y+1)];
      tmp += char_buff[scale_img(x, y+1)];
      tmp += char_buff[scale_img(x-1, y+1)];
      
      buff_tmp[scale_img(x, y)] = max(tmp/9, char_buff[scale_img(x, y)]);
    }
  }

  copy_img(buff_tmp, char_buff);
}

void img_normalize(){
  uint8_t buff_tmp[28*28];
  uint16_t max_val;

  max_val = 0;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      max_val = max(max_val, char_buff[scale_img(x, y)]);
    }
  }

  float d = 255.0/max_val;

  for(uint8_t x=0; x<28; x++){
    for(uint8_t y=0; y<28; y++){
      char_buff[scale_img(x, y)] *= d;
    }
  }

  
}


void setup() {
    uint16_t tmp;
    Serial.begin(9600);

    tft.reset();
    identifier = 0x9341;

    TS_LEFT = 130; TS_RT = 941; TS_TOP = 132; TS_BOT = 902;
    SwapXY = 1; //mods

    switch (Orientation) {      // adjust for different aspects
        case 0:   break;        //no change,  calibrated for PORTRAIT
        case 1:   tmp = TS_LEFT, TS_LEFT = TS_BOT, TS_BOT = TS_RT, TS_RT = TS_TOP, TS_TOP = tmp;  break;
        case 2:   SWAP(TS_LEFT, TS_RT);  SWAP(TS_TOP, TS_BOT); break;
        case 3:   tmp = TS_LEFT, TS_LEFT = TS_TOP, TS_TOP = TS_RT, TS_RT = TS_BOT, TS_BOT = tmp;  break;
    }

    Serial.begin(9600);
    ts = TouchScreen(XP, YP, XM, YM, 300);     //call the constructor AGAIN with new values.
    tft.begin(identifier);
    //show_Serial();
    tft.setRotation(Orientation);
    tft.fillScreen(BLACK);

    tft.drawRect(0, 0, 28*4+1, 28*4+1, WHITE);

    tft.setTextColor(CYAN);
    tft.setCursor(0, 150);
    tft.setTextSize(2);
    tft.print(F("RECOGNIZE"));

    tft.setCursor(0, 200);
    tft.print(F("CLEAR"));
    
    currentcolor = RED;
    delay(100);


    for(tmp=0; tmp<28*28; tmp++){
      char_buff[tmp]=0;
    }
    
}

void show_small_img(uint8_t off){
  uint16_t x,y;
  uint16_t color;
  
  for(x=0; x<28; x++){
    for(y=0; y<28; y++){
      color = char_buff[scale_img(x, y)];
      tft.fillCircle(x+161, y+1+off, 1, convertGREY(color));
    }
  }
  tft.drawRect(160, 0+off, 29, 29, WHITE);
}

void show_small_img2(uint8_t off){
  uint16_t x,y;
  uint16_t color;
  
  for(x=0; x<28; x++){
    for(y=0; y<28; y++){
      color = char_buff[scale_img(x, y)];
      tft.fillCircle(x*2+161-28, y*2+1+off, 2, convertGREY(color));
      
    }
  }
  tft.drawRect(160-28, 0+off, 29+28, 29+28, WHITE);
}


void loop() {
    uint16_t xpos, ypos;  //screen coordinates
    tp = ts.getPoint();   //tp.x, tp.y are ADC values



    // if sharing pins, you'll need to fix the directions of the touchscreen pins
    pinMode(XM, OUTPUT);
    pinMode(YP, OUTPUT);
    pinMode(XP, OUTPUT);
    pinMode(YM, OUTPUT);

    if (tp.z > MINPRESSURE && tp.z < MAXPRESSURE) {
        // is controller wired for Landscape ? or are we oriented in Landscape?
        if (SwapXY != (Orientation & 1)) SWAP(tp.x, tp.y);
        // scale from 0->1023 to tft.width  i.e. left = 0, rt = width
        // most mcufriend have touch (with icons) that extends below the TFT
        // screens without icons need to reserve a space for "erase"
        // scale the ADC values from ts.getPoint() to screen values e.g. 0-239
        xpos = map(tp.x, TS_LEFT, TS_RT, 0, tft.width());
        ypos = map(tp.y, TS_TOP, TS_BOT, 0, tft.height());

        if (xpos>=1 && xpos<=28*4+1 && ypos>=1 && ypos<=28*4+1) {
          tft.fillCircle(xpos, ypos, PENRADIUS, currentcolor);
          points++;
          char_buff[scale_img((xpos-1)/4, (ypos-1)/4)] = 255;
        } else {
          //tft.setCursor(0, 200);
          //tft.print("x=" + String(xpos) + "  y="+String(ypos));
        }

        if (ypos>120 && ypos < 150 && xpos<100){
          tft.setCursor(160, 200);
          tft.print("points=" + String(points));
          //tft.setTextColor(WHITE);
          show_small_img(0);
          img_move_to_corner();
          show_small_img(30);
          img_scale_from_corner();
          show_small_img(60);
          img_weighted_center();
          show_small_img(90);
          img_smooth();
          show_small_img2(120);
          //img_normalize();
          //show_small_img(150);

          
          int result = evaluate_tree(char_buff);
          tft.setTextColor(GREEN);
          tft.setCursor(200, 50);
          tft.setTextSize(3);
          tft.print("TREE");
          tft.setCursor(250, 80);
          tft.print(String(result));
          
          result = evaluate_network(char_buff);
          tft.setCursor(200, 130);
          tft.setTextSize(3);
          tft.print("NEURAL");
          tft.setCursor(250, 160);
          tft.print(String(result));


          /*
          result = evaluate_bayes(char_buff);
          tft.setCursor(200, 180);
          tft.setTextSize(3);
          tft.print("BAYES");
          tft.setCursor(250, 240);
          tft.print(String(result));
         */
        }

        if (ypos>170 && ypos < 200 && xpos<100){
          setup();
        }

        
    }
}
