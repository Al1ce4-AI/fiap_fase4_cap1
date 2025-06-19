#include <Arduino.h>
#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>

// ===== DEFINIÇÕES DE PINOS =====
#define BUTTON_P        5     // Botão fósforo (GPIO5)
#define BUTTON_K        4     // Botão potássio (GPIO4)
#define LDR_PIN        14     // Pino LDR (GPIO14)
#define DHTPIN         12     // DHT22 (GPIO12)
#define DHTTYPE       DHT22
#define RELAY_PIN      34     // Relé (GPIO34)
#define LED_PIN         2     // LED (GPIO2)
#define BUTTON_API     18     // Botão API (GPIO18)

// Objetos globais
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ===== VARIÁVEIS DE ESTADO =====
volatile uint8_t estadoFosforo = 0;    // 0 = OFF, 1 = ON
volatile uint8_t estadoPotassio = 0;
volatile uint8_t estadoAPI = 0;
uint8_t ultimoEstadoFosforo = HIGH;
uint8_t ultimoEstadoPotassio = HIGH;
uint8_t ultimoEstadoAPI = HIGH;

void setup() {
  Serial.begin(115200);
  
  // LCD - Inicialização
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(F("FarmTech Sol."));
  lcd.setCursor(0, 1);
  lcd.print(F("Otimizado v1.0"));
  delay(1500);
  
  // Configuração de pinos
  const uint8_t inputPins[] = {BUTTON_P, BUTTON_K, BUTTON_API};
  for(uint8_t i = 0; i < 3; i++) {
    pinMode(inputPins[i], INPUT_PULLUP);
  }
  
  const uint8_t outputPins[] = {RELAY_PIN, LED_PIN};
  for(uint8_t i = 0; i < 2; i++) {
    pinMode(outputPins[i], OUTPUT);
    digitalWrite(outputPins[i], LOW);
  }

  dht.begin();
}

void loop() {
  // LEITURA DE BOTÕES
  uint8_t leituraAtual;
  
  leituraAtual = digitalRead(BUTTON_P);
  if(leituraAtual == LOW && ultimoEstadoFosforo == HIGH) {
    estadoFosforo = !estadoFosforo;
    delay(150);
  }
  ultimoEstadoFosforo = leituraAtual;

  leituraAtual = digitalRead(BUTTON_K);
  if(leituraAtual == LOW && ultimoEstadoPotassio == HIGH) {
    estadoPotassio = !estadoPotassio;
    delay(150);
  }
  ultimoEstadoPotassio = leituraAtual;

  leituraAtual = digitalRead(BUTTON_API);
  if(leituraAtual == LOW && ultimoEstadoAPI == HIGH) {
    estadoAPI = !estadoAPI;
    delay(150);
  }
  ultimoEstadoAPI = leituraAtual;

  // LEITURA DE SENSORES
  uint16_t ldrValue = analogRead(LDR_PIN);
  float umidade = dht.readHumidity();
  float phSimulado = ldrValue / 100.0f;

  // CÁLCULOS
  uint8_t condicoesCriticas = 0;
  condicoesCriticas += !estadoFosforo;
  condicoesCriticas += !estadoPotassio;
  condicoesCriticas += (ldrValue > 700);
  condicoesCriticas += (umidade < 60.0f);

  uint8_t irrigacaoAtiva = (condicoesCriticas >= 2 && !estadoAPI);
  digitalWrite(RELAY_PIN, irrigacaoAtiva);
  digitalWrite(LED_PIN, irrigacaoAtiva);

  // ATUALIZAÇÃO DO LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(F("U:")); 
  lcd.print(umidade, 1);
  lcd.print(F("% pH:"));
  lcd.print(ph, 1);

  lcd.setCursor(0, 1);
  lcd.print(F("F:")); 
  lcd.print(estadoFosforo ? F("Y") : F("N"));
  lcd.print(F(" K:"));
  lcd.print(estadoPotassio ? F("Y") : F("N"));
  lcd.print(F(" I:"));
  lcd.print(irrigacaoAtiva ? F("ON") : F("--"));

  // SAÍDA SERIAL
  static char buffer[80];
  snprintf(buffer, sizeof(buffer),
    "F:%d | K:%d | pH:%.1f | U:%.1f%% | I:%s | API:%s",
    estadoFosforo, estadoPotassio, phSimulado, umidade,
    irrigacaoAtiva ? "ON" : "OFF",
    estadoAPI ? "RAIN" : "SUN"
  );
  Serial.println(buffer);

  delay(800);
}