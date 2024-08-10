#define RED_PIN 3
#define GREEN_PIN 5
#define BLUE_PIN 6

int sample_rate = 32000; // Taxa de amostragem em Hz
const int micPin = A0;       // Pino analógico onde o microfone está conectado

String command = "";

int red = 0;
int green = 0;
int blue = 0;

void setup() {
  // Iniciando comunicação serial
  Serial.begin(250000);

  // Definindo os pinos RGB 
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if (Serial.available()) {
    command = Serial.readStringUntil(':');

    if (command.equals("LISTEN")) {
      sample_rate = Serial.readStringUntil(':').toInt();
      digitalWrite(LED_BUILTIN, HIGH);
      while (!Serial.available()) {
        int sample = analogRead(micPin);
        Serial.write(sample & 0xFF); // Envia byte menos significativo
        Serial.write((sample >> 8) & 0xFF); // Envia byte mais significativo
        delayMicroseconds(1000000 / sample_rate); // Atraso para manter a taxa de amostragem
      }
    }
    if (command.equals("CHANGE COLOR")) {
      red = Serial.readStringUntil(':').toInt();
      green = Serial.readStringUntil(':').toInt();
      blue = Serial.readStringUntil(':').toInt();  

      analogWrite(RED_PIN, red);
      analogWrite(GREEN_PIN, green);
      analogWrite(BLUE_PIN, blue); 
    }
  }
}
