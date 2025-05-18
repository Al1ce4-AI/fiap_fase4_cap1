import requests
from time import sleep

def obter_dados_clima(cidade, api_key="de1bb26d32dfb587a64ca1c564b22d8a", tentativas=3):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br"
    }

    for tentativa in range(tentativas):
        try:
            resposta = requests.get(base_url, params=params, timeout=10)
            dados = resposta.json()

            if resposta.status_code == 200:
                condicao = dados["weather"][0]["description"].lower()
                main = dados["weather"][0]["main"].lower()

                chuva_detectada = (
                    "rain" in dados or
                    "chuva" in condicao or
                    "garoa" in condicao or
                    main in ["rain", "drizzle", "thunderstorm"]
                )

                return {
                    "temperatura": dados["main"]["temp"],
                    "umidade_ar": dados["main"]["humidity"],
                    "condicao": condicao,
                    "chuva": chuva_detectada
                }

            else:
                print(f"Erro na API (tentativa {tentativa + 1}): {dados.get('message', 'Erro desconhecido')}")

        except requests.exceptions.RequestException as e:
            print(f"Falha na conexão (tentativa {tentativa + 1}): {e}")

        if tentativa < tentativas - 1:
            sleep(2)

    return None


if __name__ == "__main__":
    API_KEY = "de1bb26d32dfb587a64ca1c564b22d8a"
    CIDADE = "São Paulo"

    clima = obter_dados_clima(CIDADE, API_KEY)

    if clima:
        print("\nDados Climáticos Atuais:")
        print(f"Temperatura: {clima['temperatura']}°C")
        print(f" Umidade do Ar: {clima['umidade_ar']}%")
        print(f"Condição: {clima['condicao'].capitalize()}")
        print(f"Chuva prevista: {'Sim' if clima['chuva'] else 'Não'}")
    else:
        print("Falha ao acessar a API. Verifique a conexão ou a chave.")
