#include "Wire.h"

const int LED_REG_CONFIG = 0x0;
const int LED_REG_COLUMNS = 0x1;
const int LED_REG_UPDATE = 0xC;
const int LED_REG_EFFECT = 0xD;
const int LED_REG_EQ = 0xF;

typedef enum LedArrayMode {
  LED_ARRAY_8X8,
  LED_ARRAY_7X9,
  LED_ARRAY_6X10,
  LED_ARRAY_5X11,
} LedArrayMode;

const int baseAddress = 0xC0 >> 1;

typedef enum TrevMode {
  MODE_SERIAL_CONTROL,
  MODE_SCAN,
  MODE_RANDOM,
} TrevMode;

TrevMode mode = MODE_SERIAL_CONTROL;

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

LEDArray leftTop(baseAddress);
LEDArray leftBottom(baseAddress | 1);
LEDArray rightTop(baseAddress | 2);
LEDArray rightBottom(baseAddress | 3);

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(3, OUTPUT);
  analogWrite(3, 0xff);   // Ready state light to max output
//  analogWrite(3, 0);  // Ready state light to min (0) output

//  lightFace(0);
//  updateAll();

  Serial.println("Hello from TREV");
  
  setBrightness(5);
}

void randomize(LEDArray& array) {
  int row = random() % 4;
  int col = random() % 7;

  if (random() % 2 == 0) {
    array.set(row, col, true);
    array.update();
  } else {
    array.set(row, col, false);
    array.update();
  }
}

void lineVert(LEDArray& array, int column) {
  for (int row = 0; row < 4; row++) {
    array.set(row, column, true);
  }
}

void lightFace(int column) {
  leftTop.clear();
  lineVert(leftTop, column);
  rightTop.clear();
  lineVert(rightTop, 6 - column);
  leftBottom.clear();
  lineVert(leftBottom, column);
  rightBottom.clear();
  lineVert(rightBottom, 6 - column);
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
}

void setBrightness(uint8_t level) {
  leftTop.brightness(level);
  rightTop.brightness(level);
  leftBottom.brightness(level);
  rightBottom.brightness(level);
}

void blinkRandomly() {
  randomize(leftTop);
  randomize(rightTop);
  randomize(leftBottom);
  randomize(rightBottom);
}

void scanEachLED() {
  for (int row = 0; row < 4; row++) {
    for (int col = 0; col < 7; col++) {
      leftTop.set(row, col, true);
      rightTop.set(row, col, true);
      leftBottom.set(row, col, true);
      rightBottom.set(row, col, true);
      leftTop.update();
      rightTop.update();
      leftBottom.update();
      rightBottom.update();
      delay(50);
      leftTop.set(row, col, false);
      rightTop.set(row, col, false);
      leftBottom.set(row, col, false);
      rightBottom.set(row, col, false);
      leftTop.update();
      rightTop.update();
      leftBottom.update();
      rightBottom.update();
    }
  }
}

void serialControl() {
//  static bool waitingForCommand = true;
  
  // Parse column to light
  while (Serial.available()) {
    char c = Serial.read();

    switch (c) {
      case 't': {
        int position = Serial.parseInt();
        
        if (position != 0 && position <= 7) {
          int column = position - 1;
          
          lightFace(column);
          updateAll();
    
          Serial.print("Targeting column ");
          Serial.println(column);
        }
        break;
      }
      case 'b': {
        int brightness = Serial.parseInt();
        
        if (brightness != 0 && brightness <= 14) {
          setBrightness(brightness);
          Serial.print("Set brightness to ");
          Serial.println(brightness);
        }
      }
    }
  }
}

void loop() {
  switch (mode) {
    case MODE_SERIAL_CONTROL:
      serialControl();
      break;
    case MODE_SCAN:
      scanEachLED();
      break;
    case MODE_RANDOM:
      blinkRandomly();
      break;
  }
}
