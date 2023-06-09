#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         13         
#define SS_PIN          5 
#define LED_PIN         16       // Pin LED
#define BUTTON_PIN      14   // definisikan pin untuk tombol
#define INDIKATOR       27
#define DENY            17
boolean terbaca = false;
boolean ready = true;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Inisiasi RFID RC522

void setup() {
  Serial.begin(9600);   // Inisiasi serial monitor
  while (!Serial);      // Tunggu serial monitor terkoneksi
  SPI.begin();          // Inisiasi koneksi SPI
  mfrc522.PCD_Init();    // Inisiasi RFID RC522
  pinMode(LED_PIN, OUTPUT); // Set pin LED sebagai output
  pinMode(BUTTON_PIN, INPUT_PULLUP);   // set pin tombol sebagai input dengan pull-up resistor
  pinMode(INDIKATOR, OUTPUT);
  pinMode(DENY, OUTPUT);

  //Serial.println("Silakan tempelkan kartu Mifare...");
}

void loop() {
  
  if (ready){

    if (terbaca){
      String inputString = Serial.readStringUntil('\n');
      if (inputString == "allow") {
        digitalWrite(LED_PIN, HIGH);
        ready = false;
      } else if (inputString == "deny") {
        digitalWrite(DENY, HIGH);
        delay(2000);
        digitalWrite(DENY, LOW);
        terbaca = false;
      }
    } else {
      delay(1000);
      digitalWrite(INDIKATOR, HIGH); // Hidupkan LED
      delay(1000);
      digitalWrite(INDIKATOR, LOW); // Hidupkan LED
    }

    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial() && !terbaca) {
      // Jika ada kartu yang terdeteksi, baca ID-nya
      //Serial.print("ID Kartu: "); 
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
      }
      Serial.println();
      terbaca = true;
      //digitalWrite(LED_PIN, HIGH); // Hidupkan LED
      //delay(1000);                 // Tunda selama 1 detik
    }
  } else {
    if (terbaca && digitalRead(BUTTON_PIN) == LOW) {  // jika tombol ditekan (nilai pin = LOW)
    terbaca = false;
    digitalWrite(LED_PIN, LOW);  // matikan LED
    Serial.println("entityPass");
    ready = true;
    }      
  }
  mfrc522.PICC_HaltA();         // Berhenti membaca kartu
}
