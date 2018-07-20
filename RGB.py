
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
import pygame
try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")

################### pins on ADC Pi Plus board
connected_pin_1 = 1
connected_pin_2 = 2
connected_pin_3 = 3
################### PARAMETERS
wait_time = 20 #amount of times it needs to be correct when checked.
v1 = 2.25
v2 = 2.5
v3 = 4.7

game_won = False


adc = ADCPi(0x6C, 0x6D, 12)


adc.read_voltage(connected_pin_1)

vb1[3][3] = [[78, 36, 60],
             [17, 70, 47] ,
             [52, 80, 17]]




int uitgespeeld = 0;
int begonnen = 0; 
int begincounter = 0;
int pluggenteller = 0;
int kleurcounter = 0;

marge = 14 ; // Hoe ver je van de correct waarde mag af zitten
int level = 1; // Welk level ben je
int totaal_levels = 3;
long time_per_level = 30*1000; // hoeveel lang heb je om het goed te doen 
long deadline = time_per_level;
int kleurkijktijd = 15;

long counter = 0; // hier wordt geteld 
vb1[3][3] = {{78, 36, 60},
                 {17, 70, 47},
                 {52, 80, 17}};

int schuifinput1 = A3;
int schuifinput2 = A4;
int schuifinput3 = A5; 

int uitVb = 2; // stuurt voorbeeld strip aan
int uitNa = 3; // stuurt nadoen strip aan

int numpixVb = 36;
int numpixNa = 36;

int vbRed, vbBleu, vbGreen; // waar de voorbeeldwaarde op gezet wordt
int red, green, blue; // variabelen waarin de kleuren staan die je na moet doen

Adafruit_NeoPixel stripVb = Adafruit_NeoPixel(numpixVb, uitVb, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripNa = Adafruit_NeoPixel(numpixNa, uitNa, NEO_GRB + NEO_KHZ800);


void setup() {
  // put your setup code here, to run once:
  pinMode(spelwinnen, OUTPUT);
  pinMode(beginnen, INPUT);
  pinMode(geluidgoed, OUTPUT);
  pinMode(geluidfout, OUTPUT);
  pinMode(pluggenbypass, INPUT_PULLUP);

  stripVb.begin();
  stripVb.show();
  
  stripNa.begin(); 
  stripNa.show();

  Serial.begin(9600);
  Serial.println("Ik ben aan.");
  delay (900);
} 


void loop() {

  if (digitalRead(pluggenbypass) == HIGH) { // PLUGGENSPEL BYPASS (van pin 9 naar GND met switch)
    pluggencounter++;
    if (pluggencounter > 8) {
      begonnen = 1;
    }
  } 

  // PLUGGENSPEL
  if (begonnen == 0) {
    
    int sensorValue1 = analogRead(A0);
    int sensorValue2 = analogRead(A1);
    int sensorValue3 = analogRead(A2);
      
    float voltage1 = sensorValue1*(5.0/1023.0);
    float voltage2 = sensorValue2*(5.0/1023.0);
    float voltage3 = sensorValue3*(5.0/1023.0);
      Serial.print("volt1 ");
      Serial.print(voltage1);
      Serial.print(" volt2 ");
      Serial.print(voltage2);
      Serial.print(" volt3 ");
      Serial.println(voltage3);
      delay(300);
      
    if (voltage1 >= 2.23 && voltage1 <= 2.33 && 
        voltage2 >= 2.40 && voltage2 <= 2.6 && 
        voltage3 >=4.6  && voltage3 <= 4.85) 
      {
      pluggenteller ++; 
      }
    else {pluggenteller = 0;}
    
    if (pluggenteller > 2)
      {
      Serial.println("yes");  
      digitalWrite(geluidgoed, HIGH);
      delay(105); 
      digitalWrite(geluidgoed, LOW);
      begonnen = 1;
      }
    } 
   // EIND PLUGGENSPEL
  


  if (uitgespeeld == 1) {
    digitalWrite(spelwinnen, HIGH);
    Serial.print("hoooooog");
  }
 
if (begonnen == 1){
  if (level == totaal_levels + 1) {
    colorNa(stripNa.Color(0, 150, 0));
    colorVb(stripVb.Color(0, 150, 0));
    Serial.println("gewonnen!");
    uitgespeeld = 1;
  }
  else {
    // put your main code here, to run repeatedly:

    // Kleur rood uitlezen verdeeld over de weerstand om de juiste waarde te geven
    if (analogRead(schuifinput1) < 100) {red = 0;}
    else if (analogRead(schuifinput1) < 800) {
      red = analogRead(schuifinput1) / 15;
    } else if (analogRead(schuifinput1) >= 800) {
      red = 50 + ((analogRead(schuifinput1) - 800) / 4); 
    }
    // kleur groen uitlezen en juiste waarde geven
    if (analogRead(schuifinput2) < 100) {green = 0;}
    else if (analogRead(schuifinput2) < 800) {
      green = analogRead(schuifinput2) / 15;
    } else if (analogRead(schuifinput2) >= 800) {
      green = 50 + ((analogRead(schuifinput2) - 800) / 4); 
    }
    // kleur blauw uitlezen en juiste waarde geven
    if (analogRead(schuifinput3) < 100) {blue = 0;}
    else if (analogRead(schuifinput3) < 800) {
      blue = analogRead(schuifinput3) / 15;
    } else if (analogRead(schuifinput3) >= 800) {
      blue = 50 + ((analogRead(schuifinput3) - 800) / 4); 
    }
     
    colorNa(stripNa.Color(red, green, blue));

    // checklevels
      if (level <= totaal_levels) {
        colorVb(stripVb.Color(vb1[level-1][0], vb1[level-1][1], vb1[level-1][2])); // zet de strip op de voorbeeldkleur 
        counter += 100;
        Serial.print(String(level) + ": tijd:" + String(counter) + " / " + String(deadline));
        Serial.print("\t\tkleuren: " + String(red) + ", " + String(green) + ", " + String(blue));
        Serial.print("\t\treading: " + String(analogRead(schuifinput1)) + ", " + String(analogRead(schuifinput2)) + ", " + String(analogRead(schuifinput3)));
        Serial.println("\t kijktijd: " + String(kleurcounter));
       
        if (checkColorValues(red, green, blue, level) == true){kleurcounter ++;}
        else {kleurcounter = 0;}
        if (kleurcounter > kleurkijktijd) {levelGehaald();}
      }
      else {
        uitgespeeld = 1;
      }
  
      // tijd is op
      if (counter >= deadline) {
        levelVerloren();
      }
      delay(10);
    }
  }
}

boolean checkColorValues(int red, int green,int blue, int level) {
  boolean redtrue = red > (vb1[level-1][0] - marge) && red < (vb1[level-1][0] + marge);
  boolean greentrue = green > (vb1[level-1][1] - marge) && green < (vb1[level-1][1] + marge);
  boolean bluetrue = blue > (vb1[level-1][2] - marge) && blue < (vb1[level-1][2] + marge);
  return redtrue && greentrue && bluetrue;
}

void colorNa(uint32_t c) {
  for(uint16_t i=0; i<stripNa.numPixels(); i++) {
    stripNa.setPixelColor(i, c);
    stripNa.show();
  }
}

void colorVb(uint32_t c) {
  for(uint16_t i=0; i<stripVb.numPixels(); i++) {
    stripVb.setPixelColor(i, c);
    stripVb.show();
  }
}

void levelGehaald() {
  Serial.println("winnen!");
  digitalWrite(geluidgoed, HIGH);
  delay(105);
  digitalWrite(geluidgoed, LOW);
  knipperLED(0, 255, 0, 250, 3);
  deadline += time_per_level; 
  level++;
}

void levelVerloren() {
  Serial.println("verloren!");
  digitalWrite(geluidfout, HIGH);
  delay(105);
  digitalWrite(geluidfout, LOW);
  knipperLED(255, 0, 0, 250, 3);
  deadline = time_per_level;
  counter = 0;
  level = 1;
}

void knipperLED(int red, int green, int blue, int delaytime, int herhaal){
  for (int i=0; i < herhaal; i++) {
//    Serial.println("aan...");
    colorNa(stripNa.Color(red, green, blue));
    colorVb(stripVb.Color(red, green, blue));
    
    delay(delaytime);
    
//    Serial.println("uit...");
    colorNa(stripNa.Color(0, 0, 0));
    colorVb(stripVb.Color(0, 0, 0));
    delay(delaytime);
  }
}