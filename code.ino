#include <Wire.h>
#include "MAX30105.h"
 #include <stdio.h>
#include "heartRate.h"

#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>

/* Set these to your desired credentials. */
const char *ssid = "apoorv";  //ENTER YOUR WIFI SETTINGS <<<<<<<<<
const char *password = "perception";

//Web address to read from
const char *host = "api.thingspeak.com";
String apiKey = "EALI0DL46C50WVKY";  //ENTER YOUR API KEY <<<<<<<<<<<

MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred
 
float beatsPerMinute;
int beatAvg;int temp;
int counter=0;

 WiFiClient client;     

void setup()
{
Serial.begin(115200);
WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  //WiFi.mode(WIFI_AP_STA);   //Both hotspot and client are enabled
  //WiFi.mode(WIFI_AP);       //Only Access point
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
Serial.println("Initializing...");
// Initialize sensor
if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
{
Serial.println("MAX30105 was not found. Please check wiring/power. ");
while (1);
}
Serial.println("Place your index finger on the sensor with steady pressure.");
 
particleSensor.setup(); //Configure sensor with default settings
particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
     
 
}
void loop()
{
counter=counter+1;
 

long irValue = particleSensor.getIR();
temp=particleSensor.getRed();
if (checkForBeat(irValue) == true)
{
//We sensed a beat!
long delta = millis() - lastBeat;
lastBeat = millis();
 
beatsPerMinute = 60 / (delta / 1000.0);
 
if (beatsPerMinute < 255 && beatsPerMinute > 20)
{
rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
rateSpot %= RATE_SIZE; //Wrap variable
 
//Take average of readings
beatAvg = 0;
for (byte x = 0 ; x < RATE_SIZE ; x++)
beatAvg += rates[x];
beatAvg /= RATE_SIZE;
}
}
 
Serial.print("IR=");
Serial.print(irValue);
Serial.print(", BPM=");
Serial.print(beatsPerMinute);
Serial.print(", Avg BPM=");
Serial.print(beatAvg);
Serial.print(", Avg temp=");
float op=(float)irValue/temp;
op=(-45.06*op+30.354)*op+180;
Serial.print(op);

if(counter==300){
 const int httpPort = 80; //Port 80 is commonly used for www
 //---------------------------------------------------------------------
 //Connect to host, host(web site) is define at top 
 if(!client.connect(host, httpPort)){
   Serial.println("Connection Failed");
 
   return; //Keep retrying until we get connected
 }
    String Link="GET /update?api_key="+apiKey+"&field1="+beatsPerMinute+","+op;  //Requeste webpage  
 
  Link = Link + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "Connection: close\r\n\r\n";                
 client.print(Link);
  Serial.print("Data is uploaded");


 int timeout=0;
 while((!client.available()) && (timeout < 1000))     //Wait 5 seconds for data
 {
   delay(10);  //Use this with time out
   timeout++;
 }

//---------------------------------------------------------------------
 //If data is available before time out read it.
 if(timeout < 500)
 {
     while(client.available()){
        Serial.println(client.readString()); //Response from ThingSpeak       
     }
 }
 else
 {
     Serial.println("Request timeout..");
 }

  
  counter=0;
  }
 
if (irValue < 50000)
Serial.print(" No finger?");
 
Serial.println();

}
