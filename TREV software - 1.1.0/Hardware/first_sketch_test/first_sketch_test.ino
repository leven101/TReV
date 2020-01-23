#include "Wire.h"

const int LED_REG_CONFIG = 0x0;
const int LED_REG_COLUMNS = 0x1;
const int LED_REG_UPDATE = 0xC;
const int LED_REG_EFFECT = 0xD;
const int LED_REG_EQ = 0xF;

const int baseAddress = 0xC0 >> 1;

class LEDArray {
private:
  uint8_t address;
  uint8_t ledRegValues[8] = {0};
public:
  LEDArray(uint8_t addr): address(addr)
    {}
  void update();
  void set(int row, int column, bool ledOn);
  void clear();
  void brightness(uint8_t level);
};

void LEDArray::update() {
  Wire.beginTransmission(address);
  Wire.write(LED_REG_UPDATE);
  Wire.write(0xFF);
  Wire.endTransmission();
}

void LEDArray::set(int row, int column, bool ledOn) {
  int reg = LED_REG_COLUMNS + column;

  if (ledOn) {
    ledRegValues[column] |= bit(row);
  } else {
    ledRegValues[column] &= ~bit(row);
  }
  
  Wire.beginTransmission(address);
  Wire.write(reg);
  Wire.write(ledRegValues[column]);
  Wire.endTransmission();
}

void LEDArray::clear() {
  for (int col = 0; col < 7; col++) {
    ledRegValues[col] = 0;

    Wire.beginTransmission(address);
    Wire.write(LED_REG_COLUMNS + col);
    Wire.write(ledRegValues[col]);
    Wire.endTransmission();
  }
}

// 15 levels of brightness
void LEDArray::brightness(uint8_t level) {
  if (level > 14) {
    level = 14;
  }
  
  uint8_t value = level < 7 ?
    8 | level
    : level - 7;
  
  Wire.beginTransmission(address);
  Wire.write(LED_REG_EFFECT);
  Wire.write(value);
  Wire.endTransmission();
}

LEDArray leftBottom(baseAddress);
LEDArray rightTop(baseAddress | 1);
LEDArray rightBottom(baseAddress | 2);  //INVERTED INDICES
LEDArray leftTop(baseAddress | 3);  //INVERTED INDICES 

void setBrightness(uint8_t level) {
  leftTop.brightness(level);
  rightTop.brightness(level);
  leftBottom.brightness(level);
  rightBottom.brightness(level);
}

void updateAll() {
  leftTop.update();
  rightTop.update();
  leftBottom.update();
  rightBottom.update();
}

void clearAll() {
  leftTop.clear();
  rightTop.clear();
  leftBottom.clear();
  rightBottom.clear();
  updateAll();
  analogWrite(3, 0);
}

void ledGridOn() {
  for (int row = 0; row < 4; row++) {
    for (int col=0; col < 7; col++) {
      leftTop.set(row, 6-col, true);
      rightTop.set(row, col, true);
      leftBottom.set(row, col, true);
      rightBottom.set(row, 6-col, true);
    }
  }
  updateAll();
}

void lightOneLED(int row=0, int col=3) {
  clearAll();
  rightTop.set(row, col, true);
  rightTop.update();
  setBrightness(0);
}

void lineVert(LEDArray& array, int column) {
  for (int row = 0; row < 4; row++) {
    array.set(row, column, true);
  }
}

const int colStart = 3; // sizing

void bassExample() {
  for (int c=colStart; c < colStart+1; c++) {
    lineVert(leftTop, 6-c);
    lineVert(rightTop, c);
  }
  updateAll();
  for (int b=14; b >= 0; b--) {
    setBrightness(b);
    delay(166);
  }
  for (int b=1; b < 15; b++) {
    setBrightness(b);
    delay(166);
  }
}

void trebleExample() {
    for (int c=colStart; c < colStart+1; c++) {
    lineVert(rightBottom, 6-c);
    lineVert(leftBottom, c);
  }
  updateAll();
  for (int b=1; b < 15; b++) {
    setBrightness(b);
    delay(166);
  }
  for (int b=14; b >= 0; b--) {
    setBrightness(b);
    delay(166);
  }
}

void blinkReadyStateLight() {
  for (int i=0; i < 5; i++) {
    analogWrite(3, 0);
    delay(1000); 
    analogWrite(3, 0xff);
    delay(500);
  }
  analogWrite(3, 0);
}

void drumBeatExample() {
  int timesToBeat [] = {0.74303855, 0.69659864, 0.69659864, 0.71981859, 0.69659864, 0.71981859};
  int len = sizeof(timesToBeat) / sizeof(timesToBeat[0]);
  for (int i=0; i < len; i++) {
    clearAll();
    delay(timesToBeat[i] * 1000);
    ledGridOn();
    delay(411.76);
  }
}

void normalizedBrightnessExample(float ratio=0.3) {
  setBrightness(0);
  int level = round(ratio * 14);
  leftTop.brightness(level);
  rightTop.brightness(level);
  leftBottom.brightness(14 - level);
  rightBottom.brightness(14 - level);
  Serial.print("Setting top LEDs brightness to ");
  Serial.println(level);
  for (int row = 0; row < 4; row++) {
    for (int col=colStart; col < colStart+2; col++) {
      leftTop.set(row, 6-col, true);
      rightTop.set(row, col, true);
      leftBottom.set(row, col, true);
      rightBottom.set(row, 6-col, true);
    }
  }
  updateAll();
}

void blinkLEDExample(const int seconds=1, const int tempo=200) {
  clearAll();
  setBrightness(10);
  for (int i=0; i<seconds; i++) {
      if (i%2==0) {
      for (int row = 1; row < 2; row++) {
        for (int col=colStart; col < colStart+1; col++) {
          leftTop.set(row, 6-col, true);
          rightTop.set(row, col, true);
          leftBottom.set(row, col, true);
          rightBottom.set(row, 6-col, true);
        }
      }
      updateAll();
      analogWrite(3, 0);
      delay(tempo);
      clearAll();
      analogWrite(3, 0x20);
      delay(1000-tempo);
    }
    else {
      clearAll();
      delay(1000);
    }
  }
  clearAll();
}

void inputFromPythonExample() {
  while (Serial.available()) {
    char c = Serial.read();
    Serial.println(c);
    switch (c) {
      case '|': {
        clearAll();
        break;
      }
      case 'b': {
        bassExample();
        break;
      }
      case 't':  {
        trebleExample();
        break;
      }
      case 'q': {
        String s = Serial.readString();
        int loc = s.indexOf("|");
        const int seconds = s.substring(0, loc).toInt();
        const float tempo = s.substring(loc+1, s.length()).toFloat();
//        Serial.println(seconds);
//        Serial.println(tempo);
        blinkLEDExample(seconds, tempo);
        break;
      }
      case 'p': {
        float brightness = Serial.parseFloat();
        normalizedBrightnessExample(brightness);
        break; 
      }
      case 'r': {
        blinkReadyStateLight();
        break;  
      }
      default: {
        Serial.println(Serial.readString());
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(3, OUTPUT);  // ready state light connection
  Serial.println("Hello from TREV");
}

void loop() {
// put your main code here, to run repeatedly:
//  lightOneLED(1, 1);
  inputFromPythonExample();
}
