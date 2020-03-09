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

void readyStateOn(const byte brightness) {
  analogWrite(3, brightness);
}

void readyStateOff() {
  analogWrite(3, 0);
}

void ledGridOn(const int brightness, const int rStart, const int rEnd, 
               const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      leftTop.set(row, 6-col, true);
      rightTop.set(row, col, true);
      leftBottom.set(row, col, true);
      rightBottom.set(row, 6-col, true);
    }
  }
  updateAll();
}

void ledGridOff() {
  leftTop.clear();
  rightTop.clear();
  leftBottom.clear();
  rightBottom.clear();
  updateAll();
}

void topOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      leftTop.set(row, 6-col, true);
      rightTop.set(row, col, true);
    }
  }
  leftTop.update();
  rightTop.update();
}

void leftTopOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      leftTop.set(row, 6-col, true);
    }
  }
  leftTop.update();
}

void rightTopOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      rightTop.set(row, col, true);
    }
  }
  rightTop.update();
}

void topOff() {
  leftTop.clear();
  rightTop.clear();
  leftTop.update();
  rightTop.update();
}

void bottomOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      leftBottom.set(row, col, true);
      rightBottom.set(row, 6-col, true);
    }
  }
  leftBottom.update();
  rightBottom.update();
}

void rightBottomOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      rightBottom.set(row, 6-col, true);
    }
  }
  rightBottom.update();
}

void leftBottomOn(const int brightness, const int rStart, const int rEnd, 
                   const int cStart, const int cEnd) {
  for (int row = rStart; row < rEnd; row++) {
    for (int col=cStart; col < cEnd; col++) {
      leftBottom.set(row, col, true);
    }
  }
  leftBottom.update();
}

void bottomOff() {
  leftBottom.clear();
  rightBottom.clear();
  leftBottom.update();
  rightBottom.update();
}

void lineVert(LEDArray& array, int column) {
  for (int row = 0; row < 4; row++) {
    array.set(row, column, true);
  }
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

void blinkRandomly(const int seconds) {
  int milliseconds = seconds * 1000;
  unsigned long currentMillis = millis();
  while (millis()  - currentMillis < milliseconds) {
    randomize(leftTop);
    randomize(rightTop);
    randomize(leftBottom);
    randomize(rightBottom);
  }
  ledGridOff();
}

// cmd code, brightness, row start, row end, col start, col end
const int numParams = 6;
int params[numParams];
boolean newData = false;

void recvParamsWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker && ndx < numParams) {
                params[ndx] = Serial.parseInt();
                ndx++;
            }
            else {
                for (int i=ndx; i<numParams; ++i) {
                  params[i] = -111;
                }
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
            params[ndx] = Serial.parseInt();
            ndx++;
        }
    }
}

void showAndExecuteCmd() {
    if (newData == true) {
        Serial.print("This just in ... ");
        for (int i=0; i<numParams; ++i) {
          Serial.print(String(params[i]) + " ");
        }
        Serial.println();
        executeCommand();
        newData = false;
    }
}

void executeCommand() {
  switch (params[0]) {
    case 1: {
      ledGridOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }      
    case 2: {
      readyStateOn(params[1]);
      break;
    }
    case 3: {
      readyStateOff();
      break;
    }
    case 4: {
      bottomOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }
    case 5: {
      rightBottomOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }
    case 6: {
      leftBottomOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }         
    case 7: {
      bottomOff();
      break;
    }
    case 8: {
      topOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }
    case 9: {
      rightTopOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }
    case 10: {
      leftTopOn(params[1], params[2], params[3], params[4], params[5]);
      break;
    }    
    case 11: {
      topOff();
      break;
    } 
    case 12: {
      blinkRandomly(params[1]);
      break;
    }     
    default: {
      clearAll();
    }
  }
}


void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(3, OUTPUT);  // ready state light connection
//  Serial.println("Hello from TREV");
  clearAll();
}

void loop() {
// put your main code here, to run repeatedly:
    recvParamsWithStartEndMarkers();
    showAndExecuteCmd();
}