#define TEMPPIN 0                         // This might be wrong pin
#define RELAY 4
#define BAUDRATE 115200
float Tpin = 0.00;

void setup() {
 // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                   // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(TEMPPIN, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
 Tpin= analogRead(TEMPPIN);
 SerialNina.println(Tpin);    
 delay(250);
 
}
