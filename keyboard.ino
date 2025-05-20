#include <Adafruit_NeoPixel.h>
#include <Arduino.h>
#include <Keyboard.h>

#define LED_PIN    9
#define LED_COUNT  20
#define BRIGHTNESS  75 

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

// Optional: map color names to RGB
uint32_t getColor(String color) {
  color.toUpperCase();
  if (color == "RED") return strip.Color(238, 43, 36);
  if (color == "GREEN") return strip.Color(100, 255, 0);
  if (color == "BLUE") return strip.Color(0, 0, 255);
  if (color == "YELLOW") return strip.Color(255, 206, 0);
  if (color == "PURPLE") return strip.Color(128, 0, 128);
  if (color == "CYAN") return strip.Color(0, 255, 255);
  if (color == "WHITE") return strip.Color(255, 255, 255);
  if (color == "OFF") return strip.Color(0, 0, 0);
  return strip.Color(255, 255, 255); // default white
}

// Button reader setup
const int rowPins[4] = {2, 3, 4, 5};  // Row pins (outputs)
const int colPins[4] = {12, 11, 10, 8};  // Column pins (inputs)
String notes[3][4] = {  // Musical notes layout for rows 1-3
  {"C", "C#", "D", "D#"},
  {"E", "F", "F#", "G"},
  {"G#", "A", "A#", "B"}
};

const int shiftButtonUpPin = 11;   // Octave up button (column 2, row 4)
const int shiftButtonDownPin = 10; // Octave down button (column 3, row 4)

bool octaveShiftUp = false;  // Flag for octave shift up
bool octaveShiftDown = false; // Flag for octave shift down

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  strip.show(); // Turn off all LEDs
  Keyboard.begin();
  // Set row pins as OUTPUT
  for (int i = 0; i < 4; i++) {
    pinMode(rowPins[i], OUTPUT);
    digitalWrite(rowPins[i], HIGH);
  }

  // Set column pins as INPUT_PULLUP (to detect button presses)
  for (int i = 0; i < 4; i++) {
    pinMode(colPins[i], INPUT_PULLUP);
  }
}


void writeLED(String input) {
  int firstSpace = input.indexOf(" ");
  int secondSpace = input.indexOf(" ", firstSpace + 1);

  String ledPart = input.substring(firstSpace + 1, secondSpace);
  String colorPart = input.substring(secondSpace + 1);
  uint32_t color = getColor(colorPart);

  if (ledPart == "ALL") {
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, color);
    }
  } else {
    // Handle list: 1,3,5
    int lastIndex = 0;
    while (lastIndex < ledPart.length()) {
      int commaIndex = ledPart.indexOf(",", lastIndex);
      if (commaIndex == -1) commaIndex = ledPart.length();
      int ledIndex = ledPart.substring(lastIndex, commaIndex).toInt() - 1;
      if (ledIndex >= 0 && ledIndex < LED_COUNT) {
        strip.setPixelColor(ledIndex, color);
      } else {
        Serial.println("Invalid LED index: " + String(ledIndex + 1));  // Provide feedback for invalid index
      }
      lastIndex = commaIndex + 1;
    }
  }
  strip.show();
}

void detectNote() {
  digitalWrite(rowPins[3], LOW); // Set row 4 to LOW (activate)
  // Check if shift buttons are pressed
  octaveShiftUp = (digitalRead(shiftButtonUpPin) == LOW);  // Button pressed means LOW
  octaveShiftDown = (digitalRead(shiftButtonDownPin) == LOW);  // Button pressed means LOW
  digitalWrite(rowPins[3], HIGH); // Set row 4 to HIGH (deactivate)

  // Loop through the rows (1 to 3 for notes, 4 for shift functionality)
  for (int r = 0; r < 4; r++) {
    digitalWrite(rowPins[r], LOW);  // Activate the current row
    for (int c = 0; c < 4; c++) {
      if (digitalRead(colPins[c]) == LOW) {  // Check if the button in the column is pressed
        if (r < 3) {  // If within the first 3 rows (notes)
          String note = String(notes[r][c]);

          // Apply octave shift if needed
          if (octaveShiftUp) {
            note += "5";
          } else if (octaveShiftDown) {
            note += "3";
          } else {
            note += "4";  // Standard octave
          }

          // Send the note information
          Keyboard.print("Note ");
          Keyboard.println(note);
        } else if (r == 3) {  // Row 4 functionality (special buttons)
          if (c == 0) {
            Keyboard.println("record_stop"); // For future function (if any)
          } else if (c == 3) {
            Keyboard.println("I"); // Change Instrument
          }
        }
      }
    }
    digitalWrite(rowPins[r], HIGH);  // Deactivate the current row
  }
  delay(20);  // Debounce delay to prevent multiple readings
}

void loop() {
  detectNote();
  // Read and process serial input
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    // Example: LED 5 GREEN or LED 1,3,5 BLUE
    if (input.startsWith("LED")) {
      writeLED(input);
    }
  }
}
