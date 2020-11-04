#define TEMPPIN A0                      // pin reading in temp sensor value                       
#define RELAY 4
#define BAUDRATE 115200
#define MAXI 180                        // approx how many samples per minute
#define MAXK 60                         // approx how many averages per hour

int i = 0;                              // begin global initializations
int k = 0;
int j = 0;

float Tarray[MAXI];                     
float Taverages[MAXK];
float TavTimeArray[MAXK];

long minute = 60000;                    // minute timing
long previousMillis = 0;
long currentMillis = 0;                 // end global initializations
long CaseTime = 0;

float Tpin = 0.00;
float T = 0.00;
float Tout = 0.00;
float Tav = 0.00;
long TavTime = 0;
float Tsum = 0.00;


void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                  // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(TEMPPIN, INPUT);
}

void loop() {
  
  currentMillis = millis();              // timer
  char command = 0;

  //if (SerialNina.available() > 0) {  
    command = SerialNina.read();           // check to see if there is a command from home server ?
  
    switch (command){                        // go to case that matches command
      
       
        case 'a':                              // case a - send averages to pi 
        
          CaseTime = millis();
          
          SerialNina.print(k);
          SerialNina.print('\t');
          SerialNina.println(CaseTime);
          
                                              // delay for 10 seconds
          for (j; j < k ; j++){

           // SerialNina.print(k);
           // SerialNina.print(",");
           // SerialNina.print('\t');
            SerialNina.print(TavTimeArray[j]);
            SerialNina.print(",");
            SerialNina.print('\t');
            SerialNina.println(Taverages[j]); 
          }

          k = 0;                               // reset k
          j = 0;                                // reset j
        break;
    
  default:                                 // if there are no commands from home server, do calculations

    if (i<MAXI) {
      Tpin= analogRead(TEMPPIN);             // Read temp value 
      T= (Tpin/1024)*3.3;                    // Callibration
      Tout = (T-0.5)*100;                    // Firouzan's equation
      Tarray[i] = Tout;                      // array of temperature value

      Tsum += Tarray[i];                     // sum of temp values

      i++;                                   // number of temp values

    }

    if(currentMillis - previousMillis > minute) {
      
      previousMillis = currentMillis;
      
      Tav = Tsum/(i+1);                    // average temperature calculations for minute
      TavTime = millis();
      Taverages[k] = Tav;                  // array of average temperatures
      TavTimeArray[k] = TavTime;
      k ++;
      i = 0;                               // reset i

      Tsum =0.00;                          // reset sums
    }
  
    break; 
  }
}
