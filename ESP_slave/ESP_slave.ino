#include "WiFi.h"
#include "AsyncUDP.h"

const char *ssid = "DESKTOP";
const char *password = "12345678";
AsyncUDP udp;

int pin_channel[19]={32,33,25,26,27,24,12,13,23,22,21,19,18,5,17,16,4,2,15};
int channel_power[16];
char channel_state[16];

unsigned char counter=0;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi Failed");
    while (1) {
      delay(1000);
    }
  }
  if (udp.listen(9988)) {
    Serial.print("UDP Listening on IP: ");
    Serial.println(WiFi.localIP());
    udp.onPacket([](AsyncUDPPacket packet) {
      unsigned char *p=packet.data();
      Serial.print("channel:");
      Serial.print((int)(p[0]-48));
      Serial.print(" state:");
      Serial.println((char)p[1]);
      switch  (p[1]){
        case 'N':
            channel_power[p[0]-48]=127;
            break;
        case 'R':
            channel_power[p[0]-48]=0;
            break;
        case 'L':
            if (channel_power[p[0]-48]+15<250){
            channel_power[p[0]-48]+=15;
            }
            break;
        case 'Q':
            if (channel_power[p[0]-48]-15>50){
            channel_power[p[0]-48]-=15;
            }
            break;

        default:
        Serial.println("error");
      }
    });
  }
}

void loop() {

counter+=2;
for (int i=0;i<16;i++){
    digitalWrite(pin_channel[i],counter<channel_power[i]);
}
}
