#include <SPI.h>
#include <RF24.h>

const uint64_t pipe = 0xE8E8F0F0E1LL;

RF24 radio(7, 8); // CE, CSN pins

int data[1];

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipe);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.setChannel(124);
  radio.stopListening();
}

void loop() {
  if (Serial.available() > 0) {
    data[0] = Serial.read();
    radio.write(data, sizeof(data));
  }
}
