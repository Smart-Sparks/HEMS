#define CURRENTPIN A1                  // initializations
#define VOLTAGEPIN A0
#define RELAY 4
#define BAUDRATE 115200

float Vpin = 0.00;
float Ipin = 0.00;
float V = 0.00;
float Vout = 0.00;
float I = 0.00;
float Iout = 0.00;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                  // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(CURRENTPIN, INPUT);
  pinMode(VOLTAGEPIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
 Vpin = analogRead(VOLTAGEPIN);      // read analog signal from voltage sesnor
 V= ((Vpin/1024)*3.3); // -(2.37-2.292);      // callibration
 Vout = (478.947*V)- 1203.376;       // Firouzan's equations

  
 Ipin=analogRead(CURRENTPIN);        // read analog signal from current sensor 
 I = (Ipin/1024)*3.3;                  // callibration
 Iout = (2.797*I) +1;        // Firouzan's equation
 
 SerialNina.print(Vpin); 
 SerialNina.print('\t');
 SerialNina.print(Vout); 
 SerialNina.print('\t');
 SerialNina.print(Ipin); 
 SerialNina.print('\t'); 
 SerialNina.println(Iout);   


 delay(2500);  
}
