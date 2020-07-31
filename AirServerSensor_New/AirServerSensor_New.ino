/*
   Сенсор для отправки данных на RPI
   AirServer

   29.07.2020
   by Vladimir Veber
*/

/*
   0 байт - адрес I2C
   1-6 байт - UID датчика
*/

/*
 * 0x01 - получить кол-во датчиков
 * 0x02 - получить UID
 * 0x03 & 0x04 - получить температуру и влажность с первого или второго датчика
 * 0xfd - задать адрес I2C
 * 0xfe - сбросить адрес I2C на 0x03
 * 0xff - задать случайный адрес I2C
 */

 /*
  * Serial
  * 
  * find -  задать рандомный адрес I2C
  * addr___ - (3 - 116) задать адрес I2C
  * uid____________ - задать UID датчика
  * dht_ - (0,1) получить температуру с датчика 1 или 2
  * __|____________ - (все цифры без знаков и пробелов) 1-ый байт - адрес I2C, остальные 6-ть байт UID
  * reset - сбросить настройки на заводские
  */

void(* resetFunc) (void) = 0;//объявляем функцию reset с адресом 0

#include <Wire.h>
#include <EEPROM.h>
#include <DHT.h>
#include "hex.h"
#include <avr/wdt.h>

#define numDHT 1
#define DHTPIN_1 3     // Digital pin connected to the DHT sensor
#define DHTTYPE_1 DHT11   // DHT 11

DHT dht[numDHT] = {DHT(DHTPIN_1, DHTTYPE_1)};

byte codeRequest = 0x00;
int temp[numDHT];
int hum[numDHT];
unsigned long lastMillis = 0;

void setup() {
  dht[0].begin();
  Wire.begin(EEPROM[0]);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  randomSeed(analogRead(A0)*analogRead(A1));
  wdt_enable(WDTO_500MS);
}

void loop() {
  wdt_reset();
  
  if (millis() - lastMillis >= 2 || lastMillis >= millis()) {
    lastMillis = millis();

    for (byte i = 0; i < numDHT; i++) {
      temp[i] = dht[i].readTemperature() * 100;
      hum[i] = dht[i].readHumidity() * 100;
    }
  }

  if (Serial.available() > 0) {
    String ser = Serial.readString();
    if (ser == "find") {
      getFreeAddr(0x03);
    }
    else if (ser.substring(0, 4) == "addr") {
      uint8_t address = ser.substring(4).toInt();
      //      Serial.print(address);
      EEPROM[0] = address;
      resetFunc();
    }
    else if (ser.substring(0, 3) == "uid") {
      byte strPos = 0;
      for (byte i = 1; i < 7; i++) {
        String strHex = ser.substring(3 + strPos, 4 + strPos) + ser.substring(4 + strPos, 5 + strPos);
        //Serial.println(strHex);
        EEPROM[i] = charToByte(strHex[0]) << 4 | charToByte(strHex[1]);
        strPos += 2;
      }
    }
    else if (ser.substring(0,3) == "dht") {
      float h = dht[ser.substring(3,4).toInt()].readHumidity();
      float t = dht[ser.substring(3,4).toInt()].readTemperature();

      Serial.print(t);
      Serial.print(h);
    }
    else if (ser.length() == 14) {
      byte eepromPos = 0;

      for (byte i = 0; i < 7; i++) {
        String hexUid = "";
        
        if (i != 0) hexUid = ser.substring(2 + eepromPos, 3 + eepromPos) + ser.substring(3 + eepromPos, 4 + eepromPos);
        else hexUid = ser.substring(0,1) + ser.substring(1,2);

        EEPROM[i] = charToByte(hexUid[0]) << 4 | charToByte(hexUid[1]);
        
        if (i != 0) eepromPos += 2;
      }

      resetFunc();
    }
    else if (ser == "reset")
      resetEEPROM();
  }
}

void resetEEPROM() {
  for (int i = 0; i < 1024; i++)
    EEPROM[i] = 0x00;

  EEPROM[0] = 0x03;
  
  for (byte i = 0; i < 6; i++)
    EEPROM[i+1] = 0x00;

  resetFunc();
}

String getUID() {
  String uid = "";

  for (byte i = 1; i < 7; i++) {
    uid.concat(EEPROM[i] < 0x10 ? "0" : "");
    uid.concat(String(EEPROM[i], HEX));
  }

  return uid;
}

void requestEvent() {
  if (codeRequest == 0x01) {
    String sendDhtNum = String(numDHT);
    Wire.write(sendDhtNum.length());
    Wire.write(sendDhtNum.c_str()); // respond with message of 6 bytes
    // as expected by master
  }
  else if (codeRequest == 0x02) {
    String sendText = getUID();
    Wire.write(sendText.length());
    Wire.write(sendText.c_str()); // respond with message of 6 bytes
  }
  else if (codeRequest == 0x03 || codeRequest == 0x04) {
    String sendDht = "";
    sendDht.concat(temp[codeRequest == 0x03 ? 0 : 1]);
    sendDht.concat(hum[codeRequest == 0x03 ? 0 : 1]);
    Wire.write(sendDht.length());
    Wire.write(sendDht.c_str());
  }
}

void receiveEvent(int howMany) {
  String receive = "";
  bool firstCode = true;
  byte code = 0x00;

  while (0 < Wire.available()) { // loop through all but the last
    if (!firstCode) {
      char c = Wire.read(); // receive byte as a character
      receive = receive + String(c);
    }
    else {
      code = (uint8_t)Wire.read();
      codeRequest = code;
      firstCode = false;
    }
  }

  delay(25);
  if (code == 0xfc) {
    getFreeAddr((byte)receive[0]);
  }
  else if (code == 0xfd) {
    EEPROM[0] = (byte)receive[0];
    resetFunc();
  }
  else if (code == 0xfe) {
    EEPROM[0] = 0x03;
    resetFunc();
  }
  else if (code == 0xff)
    getFreeAddr(0x03);
}

void getFreeAddr(byte startAddr) {
  uint8_t addr = random(startAddr, 0x77);

  EEPROM[0] = addr;
  Serial.println(addr);
  resetFunc();
}
