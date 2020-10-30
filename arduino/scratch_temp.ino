#define TEMPPIN A0                      // pin reading in temp sensor value                       
#define RELAY 4
#define BAUDRATE 115200
#define MAXI 69000                      // approx how many samples per minute
#define MAXK 60                         // approx how many averages per hour

long minute = 60000;                   // minute timing
long previousMillis = 0;
long currentMillis = 0;

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
 int k = 0;                               // index for minutes
 int j = 0;                               // index for looping through minute averages
 
 while (1) {                              // big loop
  
  int i =0;                               // index for samples / minute 
  float Tpin = 0.00;                      // begin inits for temp calculations
  float T =0.00;
  float Tout = 0.00;
  float Tarray[MAXI];
  float Tsum = 0.00;
  float Tav = 0.00;
  float Taverages[MAXK];                  //end inits for temp calculations
 
  while (1) {                             // inner loop
   // delay () -- might need this
   currentMillis = millis();              // timer
 
   Tpin= analogRead(TEMPPIN);
   T= (Tpin/1024)*3.3;                    // Callibration
   Tout = (T-0.5)*100;                    // Firouzan's equation
   Tarray[i] = Tout;                      // array of temperature values
     
   Tsum += Tarray[i];                     // sum of temp values

   i++;                                   // number of temp values

    // If a minute passes, break out of the loop 
    if(currentMillis - previousMillis > minute) {
    previousMillis = currentMillis;   
    break; 
    }
  }
  
  Tav = Tsum/i;                          //average temperature calculations for minute
  Taverages[k] = Tav;                    //array of average temperatures
   
  if (SerialNina.available()){           // When bluetooth seial connection is available, send data
    //SerialNina.print("Inside if statement"); // checking if entered loop
     // for ( j; j < k ; j++){
      // SerialNina.print("Inside for loop");  //checking if entered loop
       SerialNina.print(j); 
       SerialNina.print('\t'); 
       SerialNina.print(Taverages[j]); 
       SerialNina.print('\t'); 
       SerialNina.println(k);   
   //  }
 //  break;                               // when data has been sent, start back at minute 0
  }
  k++;                                 // if bluetooth connection is not available, increment minute, stay in temp calc loop
 }
}
