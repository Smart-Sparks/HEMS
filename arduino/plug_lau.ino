#define CURRENTPIN A1                        // initializations
#define VOLTAGEPIN A0
#define RELAY 12
#define BAUDRATE 115200
#define MAXK 60
#define MAXI 180

float Vrm = 0.00;
float Vrms = 0.00;
float Irm = 0.00;
float Irms = 0.00;
float S = 0.00;
float pf = 0.00;
float Power = 0.00;
float RealP = 0.00;

long minute = 60000;                   // minute timing
long previousMillis = 0;
long currentMillis = 0;
long ktime = 0;

int j =0;
int i =0;
int k = 0;

float Varray[MAXI];          
float Iarray[MAXI];            
float Vr[MAXI];
float Ir[MAXI];
float P[MAXI];

struct comp
  {
    float cAvgTime;
    float cVrms;
    float cIrms;
    float cRealP;
    float cApparentP;
    float cS;
    float cpf;
  };    
comp p[MAXK]; 

float Vpin = 0.00;
float V = 0.00; 
float Vout = 0.00;

float Ipin = 0.00;
float I = 0.00;
float Iout = 0.00;
 
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                     // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(CURRENTPIN, INPUT);
  pinMode(VOLTAGEPIN, INPUT);
  digitalWrite(RELAY, LOW); // normally closed
}

void loop() {
  
  currentMillis = millis();   
  char command = 'z'; // for incoming serial data
  
  //if (Serial.available() > 0) {           // if Serial connection is avaialbe:
     
    command = SerialNina.read();              // check for command from user 
    switch (command){
       
      case 'a':                          // case a - send data to home server 
        for(j; j<k; j++){
          SerialNina.print(p[j].cAvgTime);
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cVrms); 
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cIrms);
          SerialNina.print('\t');
          SerialNina.print(p[j].cRealP); 
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cS);
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cpf);
          SerialNina.print('\t'); 
          SerialNina.println(j);
        }
          
        k = 0;                            // reset values after sending data to home server 
        j = 0;
          
     break;
        
     case 'b':                                   // case b - toggle really - disconnect load 
      digitalWrite(RELAY,HIGH);
      SerialNina.println("Relay toggled");
      break;

     case 'c':                                   // case c - toggle relay - reconnect load 
      digitalWrite(RELAY,LOW);
      SerialNina.println("Relay toggled");
      break;


     default:
      if (i<MAXI){
        Ipin=analogRead(CURRENTPIN);          // read analog signal from current sensor 
        I = (Ipin/1024)*3.3;                  // callibration
        Iout = (2.797*I) +1;                  // Firouzan's equation
        Iarray[i] = Iout;                     // store all current values in array 

        Vpin = analogRead(VOLTAGEPIN);        // read analog signal from voltage sesnor
        V= ((Vpin/1024)*3.3); // -(2.37-2.292);      // callibration
        Vout = (478.947*V)- 1203.376;         // Firouzan's equations
        Varray[i] = Vout;                     // store all voltage values in array 

        Ir[i] = Iarray[i]*Iarray[i];          // Computing Irms  - sum(Isample^2)
        Irm += Ir[i];                

        Vr[i] = Varray[i]*Varray[i];          // Computing Vrms - sum(Vsample^2)
        Vrm += Vr[i];   

        P[i] = Varray[i] * Iarray[i];         // Computing real power - sum(V*I)
        Power += P[i];
    
        i ++;                                 // counts how many times the while loop executes - the size of the arrays
        }
    
      if(currentMillis - previousMillis > minute) {
        previousMillis = currentMillis;
    
        ktime = millis();                     //Time of af averages
        p[k].cAvgTime = ktime;

        Vrms = sqrt(Vrm/(i+1));               // Computing Vrms
        p[k].cVrms = Vrms;          
        
        Irms = sqrt(Irm/(i+1));               // Computing Irms
        p[k].cIrms = Irms;  
   
        RealP = Power/(i+1);                  // Computing Average Real Power  --- need to rethink
        p[k].cRealP = RealP;

        S = Vrms * Irms;                      // Computing apparent power
        p[k].cS = S;
 
        pf = RealP/S;                         // Computing power factor 
        p[k].cpf = pf;

        k++;
        
        i = 0;                               // reset sampling index after minute (override arrays)

        Vrm = 0.00;                          // reset sums after minute
        Irm = 0.00;
        Power = 0.00;
      }
    break;
    }
}      
