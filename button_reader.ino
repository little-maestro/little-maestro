 
 // instal Arduino Extension pack (ctrl+shift+x  search auduino install Arduino by moozzyk)
const int rowPins[4] = {20, 21, 23, 24};  // Row pins (outputs)
const int colPins[4] = {30, 29, 28, 27};  // Column pins (inputs)
char notes[3][4] = {  // Musical notes layout for rows 1-3
  {'C', 'C#', 'D', 'D#'},
  {'E', 'F', 'F#', 'G'},
  {'G#', 'A', 'A#', 'B'}
};

const int shiftButtonUpPin = 29;   // Octave up button (column 2, row 4)
const int shiftButtonDownPin = 28; // Octave down button (column 3, row 4)

bool octaveShiftUp = false;  // Flag for octave shift up
bool octaveShiftDown = false; // Flag for octave shift down

void setup() {
    Serial.begin(9600);

  // Set row pins as OUTPUT
  for (int i = 0; i < 4; i++) {
    pinMode(rowPins[i], OUTPUT);
    digitalWrite(rowPins[i], HIGH)
  }

  // Set column pins as INPUT_PULLUP (to detect button presses)
  for (int i = 0; i < 4; i++) {
    pinMode(colPins[i], INPUT_PULLUP);
  }
}


void loop() {
  digitalWrite(rowPins[3], LOW) // Set row 4 to LOW (activate)
  // Check if shift buttons are pressed
  octaveShiftUp = (digitalRead(shiftButtonUpPin) == LOW);  // Button pressed means LOW
  octaveShiftDown = (digitalRead(shiftButtonDownPin) == LOW);  // Button pressed means LOW
  digitalWrite(rowPins[3], HIGH) // Set row 4 to HIGH (deactivate)

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
          }
            else {
            note += "4"
          }

          // Send the note information
          Serial.println(note);
        } else if (r == 3) {  // Row 4 functionality (special buttons)
          if (c == 0) {
            Serial.println("o"); // For future function (if any)
          } else if (c == 3) {
            Serial.println("I"); // Change Instrument
          }
        }
      }
    }
    digitalWrite(rowPins[r], HIGH);  // Deactivate the current row
  }
  delay(200);  // Debounce delay to prevent multiple readings
}
