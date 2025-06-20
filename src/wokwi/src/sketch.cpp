// ===== INCLUDES =====
#include <Arduino.h>
#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===== DEFINIÇÕES DE PINOS =====
constexpr uint8_t BUTTON_P      = 5;   // Botão fósforo (GPIO5)
constexpr uint8_t BUTTON_K      = 4;   // Botão potássio (GPIO4)
constexpr uint8_t LDR_PIN       = 32;  // Pino LDR (GPIO32)
constexpr uint8_t DHTPIN        = 12;
constexpr uint8_t RELAY_PIN     = 25;
constexpr uint8_t LED_PIN       = 2;
constexpr uint8_t BUTTON_API    = 18;
constexpr auto    DHTTYPE       = DHT22;

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(39, 16, 2);

volatile uint8_t estadoFosforo    = 0;
volatile uint8_t estadoPotassio   = 0;
uint8_t ultimoEstadoFosforo       = HIGH;
uint8_t ultimoEstadoPotassio      = HIGH;

// ===== PROTÓTIPOS DE FUNÇÃO =====
void atualizarLCD(float& umidade, float& ph, bool& irrigStatus);
void logSerial(float& umidade, float& ph, bool& irrigStatus);


void print_lcd_and_serial(const String& message) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(message);
  Serial.println(message);
}

// === CONFIGURAÇÃO DE REDE E API ===
const char* ssid = NETWORK_SSID;
const char* password = NETWORK_PASSWORD;
const int canal_wifi = 6; // Canal do WiFi (no uso real, deixar automático)
const char* endpoint_api = API_URL; // URL da API
const String init_sensor = String(endpoint_api) + "/init/";     // Endpoint de inicialização
const String post_sensor = String(endpoint_api) + "/leitura/";  // Endpoint de envio de dados
const String verificar_irrigacao = String(endpoint_api) + "/irrigacao/";  // Endpoint de envio de dados

// === FUNÇÃO DE CONEXÃO WI-FI ===
void conectaWiFi() {
  WiFi.begin(ssid, password, canal_wifi);
  print_lcd_and_serial("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  print_lcd_and_serial("WiFi conectado!");
}

// === FUNÇÃO DE ENVIO DE DADOS PARA API ===
int post_data(JsonDocument& doc, const String& endpoint_api) {
  Serial.println("Enviando dados para a API: " + endpoint_api);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(endpoint_api);

    String jsonStr;
    serializeJson(doc, jsonStr);
    int httpCode = http.POST(jsonStr);

    if (httpCode > 0) {
      Serial.println("Status code: " + String(httpCode));
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.println("Erro na requisição");
    }
    http.end();
    return httpCode;
  } else {
    Serial.println("WiFi desconectado, impossível fazer requisição!");
  }

  return -1; // Retorna -1 se não conseguiu enviar os dados

}

// === FUNÇÃO DE VERIFICAÇÃO DE IRRIGAÇÃO ===
int should_irrigate(JsonDocument& doc) {
   Serial.println("Enviando dados para a API: " + verificar_irrigacao);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(verificar_irrigacao);

    String jsonStr;
    serializeJson(doc, jsonStr);
    int httpCode = http.POST(jsonStr);

    if (httpCode > 0) {
      Serial.println("Status code: " + String(httpCode));
      String payload = http.getString();
      JsonDocument resposta;
      DeserializationError erro = deserializeJson(resposta, payload);
      if (!erro) {
        bool irrigar = resposta["irrigar"];
        if (irrigar){
          return 1; // Retorna 1 se deve irrigar
        } else {
          return 0; // Retorna 0 se não deve irrigar
        }
      } else {
        Serial.println("Erro ao converter payload em JSON");
        return -1; // Retorna -1 se houve erro na conversão
      }
      } else {
        Serial.println("Erro na requisição");
      }
    http.end();
    return 0;
  } else {
    Serial.println("WiFi desconectado, impossível fazer requisição!");
  }

  return -1; // Retorna -1 se não conseguiu enviar os dados
}

// === IDENTIFICAÇÃO DO DISPOSITIVO ===
char chipidStr[17];
bool iniciou_sensor = false;

void iniciar_sensor() {
  uint64_t chipid = ESP.getEfuseMac();
  sprintf(chipidStr, "%016llX", chipid);
  print_lcd_and_serial("Chip ID: " + String(chipidStr));

  JsonDocument doc;
  doc["serial"] = chipidStr; // Adiciona o Chip ID ao JSON
  int httpcode = post_data(doc, init_sensor); // Envia o Chip ID para a API

  if (httpcode >= 200 && httpcode < 300) {
    print_lcd_and_serial("Sensor iniciado com sucesso!");
    delay(1000); // delay para garantir que a mensagem seja visível
    iniciou_sensor = true;
  } else {
    print_lcd_and_serial(String("Falha ao iniciar o sensor na API: ") + String(httpcode));
    delay(1000); // delay para garantir que a mensagem seja visível
  }
}



void setup() {
  // Serial otimizada (115200 é padrão para ESP32)
  Serial.begin(115200);

  // LCD - Inicialização otimizada
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(F("FarmTech Sol."));  // F() para armazenar na Flash
  lcd.setCursor(0, 1);
  lcd.print(F("Otimizado v1.0"));
  delay(1500);  // Reduzido de 2500ms

  // Configuração de pinos (agrupada por tipo)
  const uint8_t inputPins[] = {BUTTON_P, BUTTON_K, BUTTON_API};
  for(uint8_t i = 0; i < 3; i++) {
    pinMode(inputPins[i], INPUT_PULLUP);
  }

  const uint8_t outputPins[] = {RELAY_PIN, LED_PIN};
  for(uint8_t i = 0; i < 2; i++) {
    pinMode(outputPins[i], OUTPUT);
    digitalWrite(outputPins[i], LOW);  // Estado inicial definido
  }

  dht.begin();


  conectaWiFi();

}

// ===== FUNÇÕES AUXILIARES =====
void atualizarLCD(float& umidade, float& ph, bool& irrigStatus) {
  lcd.clear();

  // Linha 1 - Dados principais (otimizado para 16 caracteres)
  lcd.setCursor(0, 0);
  lcd.print(F("U:"));
  lcd.print(umidade, 1);
  lcd.print(F("% pH:"));
  lcd.print(ph, 1);

  // Linha 2 - Estados (usando símbolos para economizar espaço)
  lcd.setCursor(0, 1);
  lcd.print(F("F:"));
  lcd.print(estadoFosforo ? F("Y") : F("N"));  // Y/N em vez de ON/OFF
  lcd.print(F(" K:"));
  lcd.print(estadoPotassio ? F("Y") : F("N"));
  lcd.print(F(" I:"));
  lcd.print(irrigStatus ? F("ON") : F("--"));
}

void logSerial(float& umidade, float& ph, bool& irrigStatus) {

  // Buffer estático para evitar alocações dinâmicas
  static char buffer[80];

  snprintf(buffer, sizeof(buffer),
    "F:%d | K:%d | pH:%.1f | U:%.1f%% | I:%s",
    estadoFosforo, estadoPotassio, ph, umidade,
    irrigStatus ? "ON" : "OFF"
    //estadoAPI ? "RAIN" : "SUN"
  );

  Serial.println(buffer);
}


void loop() {

  if (!iniciou_sensor) {
    iniciar_sensor();
  }


  JsonDocument doc;
  doc["serial"] = chipidStr; // Adiciona o Chip ID ao JSON


  // === LEITURA DE BOTÕES (OTIMIZADA) ===
  uint8_t leituraAtual;

  leituraAtual = digitalRead(BUTTON_P);
  if(leituraAtual == LOW && ultimoEstadoFosforo == HIGH) {
    estadoFosforo = !estadoFosforo;
    delay(150);  // Debounce reduzido
  }
  ultimoEstadoFosforo = leituraAtual;

  leituraAtual = digitalRead(BUTTON_K);
  if(leituraAtual == LOW && ultimoEstadoPotassio == HIGH) {
    estadoPotassio = !estadoPotassio;
    delay(150);
  }
  ultimoEstadoPotassio = leituraAtual;

  //leituraAtual = digitalRead(BUTTON_API);
  //if(leituraAtual == LOW && ultimoEstadoAPI == HIGH) {
  //  estadoAPI = !estadoAPI;
  //  delay(150);
  //}
  //ultimoEstadoAPI = leituraAtual;

  // === LEITURA DE SENSORES ===
  uint16_t ldrValue = analogRead(LDR_PIN);  // uint16_t para valores 0-4095
  float umidade = dht.readHumidity();
  float phSimulado = (ldrValue / 4095.0f) * 14.0f;     // 'f' para float literal

  // === CÁLCULOS OTIMIZADOS ===
  uint8_t condicoesCriticas = 0;
  condicoesCriticas += !estadoFosforo;
  condicoesCriticas += !estadoPotassio;
  condicoesCriticas += (ldrValue > 700);
  condicoesCriticas += (umidade < 60.0f);

  bool irrigacaoAtiva_local = condicoesCriticas >= 2;

  doc["umidade"] = umidade;  // Adiciona umidade ao JSON
  doc["ph"] = phSimulado;     // Adiciona pH simulado
  doc["estado_fosforo"] = estadoFosforo;  // Adiciona estado do fósforo
  doc["estado_potassio"] = estadoPotassio; // Adiciona estado do potássio
  doc["estado_api"] = false; // Adiciona estado da API
  doc["estado_irrigacao"] = irrigacaoAtiva_local; // Adiciona estado da irrigação

  int resposta_irrigacao = -1; // Inicializa com -1 para indicar erro

  if (iniciou_sensor) {
    // Envia os dados para a API
    int httpcode = post_data(doc, post_sensor);
    if (httpcode >= 200 && httpcode < 300) {
      Serial.println("Dados enviados com sucesso!");
    } else {
      Serial.println("Falha ao enviar dados.");
    }

    resposta_irrigacao = should_irrigate(doc);
    if (resposta_irrigacao == -1) {
      Serial.println("Erro ao verificar irrigação na API, usando lógica local.");
    } else {
      Serial.println("Resposta da API: " + String(resposta_irrigacao));
    }
  }

  // Determina o estado da irrigação
  bool irrigacaoAtiva = irrigacaoAtiva_local;

  if (resposta_irrigacao != -1) {
    // Se a resposta da API for válida, usa ela
    irrigacaoAtiva = resposta_irrigacao == 1;
  }


  digitalWrite(RELAY_PIN, irrigacaoAtiva);
  digitalWrite(LED_PIN, irrigacaoAtiva);

  // === ATUALIZAÇÕES DE SAÍDA ===
  atualizarLCD(umidade, phSimulado, irrigacaoAtiva);
  logSerial(umidade, phSimulado, irrigacaoAtiva);

  // Delay otimizado (poderia usar millis() para não-blocking)
  delay(2000);  // Delay modificado para 2 segundos, suficiente para leituras e atualizações
}
