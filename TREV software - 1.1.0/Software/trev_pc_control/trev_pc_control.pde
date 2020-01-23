/*
TREV headset prototype client software.
Visualization of the state of the LEDs on the headset and
controls the target column.

LED controls:
- Up arrow key, or the w key: move the lighted column towards
  the back of the user's head
- Down arrow key, or the s key: move the lighted column towards
  the front of the user's head

View controls:
- Scroll: zoom
- Middle click: pan
- Click and drag: rotate around center

Headset communication protocol: send the column that should
be lit as an ASCII number between 1 and 7 (inclusive).
*/

import saito.objloader.*;
import peasy.PeasyCam;
import processing.serial.*;

PeasyCam cam;
OBJModel trevModel;

int currentColumn = 0;
int brightness = 0; 

int arraySeparation = 80;

Serial port;
boolean headsetConnected = false;

void setup() {
  //size(800, 800, P3D);
  fullScreen(P3D);
  background(0);
  lights();
  
  // Try to connect to the headset
  try {
    port = new Serial(this, "/dev/cu.SLAB_USBtoUART", 115200);
    headsetConnected = true;
  } catch(RuntimeException e) {
    println("Headset not connected");
  }
    
  cam = new PeasyCam(this, 100);
  
  // Load a 3D model of the headset
  trevModel = new OBJModel(this, "trev.obj", "relative", TRIANGLES);
  trevModel.shapeMode(LINES);
  trevModel.scale(0.5);
}

void draw() {
  background(0);
  
  // Draw the headset
  pushMatrix();
  rotateY(-PI / 2);
  translate(-arraySeparation / 2, 6, 5);
  stroke(127);
  trevModel.draw();
  popMatrix();
  
  // Draw the LED arrays
  pushMatrix();
  translate(5, 0, 0);
  drawArray(currentColumn, 8, 7);
  rotateY(PI);
  translate(0, 0, arraySeparation);
  drawArray(6 - currentColumn, 8, 7);
  popMatrix();
}

void keyPressed() {
  if (key == ' ') {
    port.write(currentColumn);
  } else if (key == 'w' || (key == CODED && keyCode == UP)) {
    if (currentColumn < 6) {
      currentColumn++;
      
      if (headsetConnected) {
        port.write("t" + currentColumn + "\r");
      }
    }
  } else if (key == 's' || (key == CODED && keyCode == DOWN)) {
    if (currentColumn > 0) {
      currentColumn--;
      
      if (headsetConnected) {
        port.write("t" + currentColumn + "\r");
      }
    }
  } else if (key == 'a' || (key == CODED && keyCode == LEFT)) {
    if (brightness > 0) {
      brightness--;
      
      if (headsetConnected) {
        port.write("b" + brightness + "\r");
      }
    }
  } else if (key == 'd' || (key == CODED && keyCode == RIGHT)) {
    if (brightness < 14) {
      brightness++;
      
      if (headsetConnected) {
        port.write("b" + brightness + "\r");
      }
    }
  }
}

void drawArray(int columnToLight, int rowCount, int columnCount) {
  noStroke();
  
  int s = 4;
  
  for (int row = 0; row < rowCount; row++) {
    for (int column = 0; column < columnCount; column++) {
      pushMatrix();
      translate(column * s - s * columnCount / 2, row * s / 2, 0);
      
      if (column == columnToLight) {
        fill(255, 0, 0);
      } else {
        fill(255, 255, 255);
      }
      
      box(1);
      popMatrix();
    }
  }
}
