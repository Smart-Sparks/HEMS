#define CURRENTPIN A1                  // initializations
#define VOLTAGEPIN A0
#define RELAY 4
#define BAUDRATE 115200
#define MAXK 60
#define MAXI 180

long minute = 60000;
long previousMillis = 0;
long currentMillis = 0;

String Read;

String send2pi;

struct comp
{
   float cVrms;
   float cIrms;
   float cRealP;
   float cApparentP;
   float cS;
   float cpf;
};                                       // initilizations end

void setup() {                          // set up begins
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(NINA_RESETN, OUTPUT);         
  digitalWrite(NINA_RESETN, HIGH);
  Serial.begin(115200);                  // Buad rate
  SerialNina.begin(115200);
  pinMode(RELAY, OUTPUT);
  pinMode(CURRENTPIN, INPUT);
  pinMode(VOLTAGEPIN, INPUT);
}                                       // set up ends

void loop() {
  int k = 0;                            // index the minute a datapoint is collected for
  int l = 0;                            // index for sendtopi
  while (1) {                           // big loop
    
    comp p[MAXK];                       // intializations - reset values each time loops
  
    int i = 0; // sample size
   
    float Vpin = 0.00;
    float V = 0.00; 
    float Vout = 0.00;
    float Varray[MAXI];       
    
    float Ipin = 0.00;
    float I = 0.00;
    float Iout = 0.00;
    float Iarray[MAXI];            

    float Vr[MAXI];
    float Ir[MAXI];
    float P[MAXI];

    float Vrm = 0.00;
    float Vrms = 0.00;
    float Irm = 0.00;
    float Irms = 0.00;
    float S = 0.00;
    float pf = 0.00;
    float Power = 0.00;
    float RealP = 0.00;                   // end initializations

    
    while (1) {                          // inner loop
      // delay () -- might need this
      currentMillis = millis();
 
      Vpin = analogRead(VOLTAGEPIN);      // read analog signal from voltage sesnor
      V= ((Vpin/1024)*3.3); // -(2.37-2.292);      // callibration
      Vout = (478.947*V)- 1203.376;       // Firouzan's equations
      Varray[i] = Vout;                   // store all voltage values in array 
  
      Ipin=analogRead(CURRENTPIN);        // read analog signal from current sensor 
      I = (Ipin/1024)*3.3;                  // callibration
      Iout = (2.797*I) +1;        // Firouzan's equation
      Iarray[i] = Iout;                   // store all current values in array 

      Vr[i] = Varray[i]*Varray[i];        // Computing Vrms - sum(Vsample^2)
      Vrm += Vr[i];   

      Ir[i] = Iarray[i]*Iarray[i];        // Computing Irms  - sum(Isample^2)
      Irm += Ir[i];                

      P[i] = Varray[i] * Iarray[i];       // Computing real power - sum(V*I)
      Power += P[i];

      i ++;                               // counts how many times the while loop executes - the size of the arrays

      // If a minute passes, break out of the loop 
      if(currentMillis - previousMillis > minute) {
      previousMillis = currentMillis;   
      break; 
      SerialNina.println("stuck in first loop");
      
      }
    }  
                   
    Vrms = sqrt(Vrm/(i+1));                   // Computing Vrms
    p[k].cVrms = Vrms;          
      
    Irms = sqrt(Irm/(i+1));                   // Computing Irms
    p[k].cIrms = Irms;  
   
    RealP = Power/(i+1);                      // Computing Average Real Power  --- need to rethink
    p[k].cRealP = RealP;

    S = Vrms * Irms;                      // Computing apparent power
    p[k].cS = S;
  
    pf = RealP/S;                         // Computing power factor 
    p[k].cpf = pf;

   // SerialNina.stream.flush();
    if (SerialNina.available()>0){          // When bluetooth seial connection is available, send data 
      //SerialNina.println("Inside first if");
      //Read = SerialNina.read();
     // if (Read = '3') {
      //SerialNina.println("Inside second if");
     // delay (5000);
     // for ( l; l < k ; l++){ 
       // SerialNina.print("Inside for");
      //  SerialNina.print(i);
      //  SerialNina.print('\t'); 
        SerialNina.print(p[k].cVrms); 
        SerialNina.print('\t'); 
        SerialNina.print(p[k].cIrms);
        SerialNina.print('\t');
        SerialNina.print(p[k].cRealP); 
        SerialNina.print('\t'); 
        SerialNina.print(p[k].cS);
        SerialNina.print('\t'); 
        SerialNina.printlnb(p[k].cpf); 
      //  SerialNina.print('\t'); 
      //  SerialNina.println(k); 
        delay(250);       
        }  
     //break; 
      } 
    k ++; 
  }
   
