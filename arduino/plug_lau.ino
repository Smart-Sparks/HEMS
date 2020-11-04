#define CURRENTPIN A1                        // initializations
#define VOLTAGEPIN A0
#define RELAY 8
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
float P = 0.00;

long minute = 60000;                   // minute timing
long previousMillis = 0;
long currentMillis = 0;
long ktime = 0;
long CaseTime = 0;

int j =0;
int i =0;
int k = 0;

struct comp
  {
    long cAvgTime;
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
float Vr = 0.00;

float Ipin = 0.00;
float I = 0.00;
float Iout = 0.00;
float Ir = 0.00;

 
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                     // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(CURRENTPIN, INPUT);
  pinMode(VOLTAGEPIN, INPUT);
  digitalWrite(RELAY, HIGH); // normally open
}

void loop() {
  
  currentMillis = millis();   
  char command = 'z'; // for incoming serial data
     
  command = SerialNina.read();              // check for command from user 
  switch (command){
       
      case 'a':                          // case a - send data to home server 

        CaseTime = millis();
        
        SerialNina.print(k);
        SerialNina.print('\t'); 
        SerialNina.println(CaseTime);
        
        for(j; j<k; j++){
          SerialNina.print(p[j].cAvgTime);
          SerialNina.print(",");
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cVrms);
          SerialNina.print(","); 
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cIrms);
          SerialNina.print(",");
          SerialNina.print('\t');
          SerialNina.print(p[j].cRealP); 
          SerialNina.print(",");
          SerialNina.print('\t'); 
          SerialNina.print(p[j].cS);
          SerialNina.print(",");
          SerialNina.print('\t'); 
          SerialNina.println(p[j].cpf);
         
        }
          
        k = 0;                            // reset values after sending data to home server 
        j = 0;
          
     break;
        
     case 'b':                                   // case b - toggle really - reconnect load 
      digitalWrite(RELAY,HIGH);
      SerialNina.println("Relay toggled");
      break;

     case 'c':                                   // case c - toggle relay - disconnect load 
      digitalWrite(RELAY,LOW);
      SerialNina.println("Relay toggled");
      break;


     default:
      //if (i<MAXI){
        Ipin=analogRead(CURRENTPIN);          // read analog signal from current sensor 
        I = (Ipin/1024)*3.3;                  // Callibration
        Iout = abs(I-2.3)/0.066;              // Firouzan's equation
       

        Vpin = analogRead(VOLTAGEPIN);        // read analog signal from voltage sesnor
        V = (Vpin/1024)*3.3;                  // Callibration
        Vout = abs(48*V);                     // Firouzan's equation
       
        Ir = Iout* Iout;                      // Computing Irms  - sum(Isample^2)
        Irm = Irm + Ir;          

        Vr = Vout * Vout;                     // Computing Vrms - sum(Vsample^2)
        Vrm = Vrm + Vr; 

        P = Iout * Vout;                      // Computing real power - sum(V*I)
        Power = Power + P;
    
        i ++;                                 // counts how many times the while loop executes - the size of the arrays
       // }
    
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
        Power = 0.0;
      }
    break;
    }
}      
