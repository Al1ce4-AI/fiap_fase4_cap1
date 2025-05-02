# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>


# Projeto: fiap_fase2_cap6

## Atividade em Grupo: FIAP - 1TIAOB - 2025/1 - Fase2 Cap6

## 👨‍🎓 Integrantes: 
- <a href="">Alice C. M. Assis - RM 566233</a>
- <a href="">Leonardo S. Souza - RM 563928</a>
- <a href="">Lucas B. Francelino - RM 561409</a> 
- <a href="">Pedro L. T. Silva - RM 561644</a> 
- <a href="">Vitor A. Bezerra - RM 563001</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="proflucas.moreira@fiap.com.br">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="profandre.chiovato@fiap.com.br">André Godoi Chiovato</a>


## 📜 Descrição

Este projeto tem como objetivo desenvolver um mini sistema de gestão de agronegócio, voltado para atender às necessidades de controle e organização no setor. A aplicação permite que o usuário:

- Cadastre fazendas, insumos e maquinários.
- Controle os custos relacionados a insumos e combustível.
- Obtenha rotas otimizadas para colheita na lavoura.

A solução utiliza conceitos de subalgoritmos, estruturas de dados (listas, tuplas, dicionários), manipulação de arquivos (texto e JSON) e conexão com banco de dados Oracle. O foco principal está na inovação, boa usabilidade e relevância para o setor do agronegócio, proporcionando uma ferramenta prática e eficiente para os usuários.

## Conceitos vistos nas aulas utilizados neste projeto:

- **Subalgoritmos**: O projeto utiliza funções e procedimentos com passagem de parâmetros para modularizar e organizar o código, promovendo reutilização e clareza. Exemplos podem ser observados em diversas partes do código, como:

  - O procedimento `main()` no arquivo [main.py](src/main.py), que organiza o fluxo principal da aplicação.
  - O procedimento `log()` no arquivo [loggers.py](src/logger/loggers.py), que implementa diferentes níveis de log com parâmetros como `message`, `level` e outros opcionais.
  - O método `execute_sql()` no arquivo [database.py](src/database/tipos_base/database.py), que executa comandos SQL com parâmetros como `sql`, `max_retries` e `commit`.
  - A função `makeRed()` no arquivo [color_text.py](src/logger/color_text.py), que transforma o texto em vermelho e devolve uma string para ser printada para o user.


  Esses subalgoritmos são fundamentais para garantir a modularidade, a reutilização de código e a manutenção eficiente do sistema.


- **Estruturas de dados**: O projeto faz uso de diferentes estruturas de dados para organizar e manipular informações de forma eficiente. Exemplos incluem:

  - **Listas**: Utilizadas para obter coleções de dados, como no arquivo [query.py](src/database/tipos_base/query.py).
  - **Tuplas**: Empregadas para representar conjuntos imutáveis de dados, como no retorno de múltiplos valores em funções no arquivo [senha.py](src/database/login/senha.py).
  - **Dicionários**: Usados para mapear pares chave-valor, como na serialização e desserialização de dados no arquivo [senha.py](src/database/login/senha.py).
  - **Tabelas de memória**: Implementadas no contexto de manipulação de dados em memória, como no uso de `pandas` para exibir e processar tabelas no arquivo [model.py](src/database/tipos_base/model.py).
  - **Classes e Dataclasses**: O arquivo [model.py](src/database/tipos_base/model.py) é um exemplo central do uso de dataclasses para representar modelos de dados. Ele utiliza:

    - **Dataclasses**: Para definir modelos de dados com campos fortemente tipados, como `id` e outros atributos específicos.
    - **Métodos utilitários**: Como `to_dict()` e `from_dict()` para converter instâncias em dicionários e vice-versa.
    - **Enums**: Para representar valores fixos e categóricos, garantindo consistência nos dados.
    - **Pandas DataFrames**: Para exibir e manipular dados em formato tabular, como no método `get_dataframe()`.


  Essas estruturas são essenciais para organizar os dados de forma clara e eficiente, permitindo que o sistema seja escalável e de fácil manutenção.


- **Manipulação de arquivos: texto e JSON**: A manipulação de arquivos é um dos pilares deste projeto, permitindo exportar e importar dados no formato JSON, além de registrar logs em arquivos de texto. Os principais arquivos relacionados a essa funcionalidade são:
    - **[loggers.py](src/logger/loggers.py)**: Responsável por registrar logs em um arquivo de texto (`log.txt`). A função `log()` permite gravar mensagens com diferentes níveis de severidade (INFO, WARNING, ERROR, etc.), enquanto as funções auxiliares (`log_info`, `log_error`, etc.) simplificam o uso. O arquivo de log é atualizado automaticamente sempre que uma mensagem é registrada.
    - **[exportar_json_generico.py](src/menu/generico/exportar_json_generico.py)**: Implementa a exportação de dados de modelos para arquivos JSON. A função `exportar_json_generico()` obtém os dados do banco de dados, os exibe em formato tabular e os salva em um arquivo JSON no diretório configurado (`EXPORTS_DIR`). Logs são gerados para informar o progresso e possíveis erros durante o processo.
    - **[importar_json_generico.py](src/menu/generico/importar_json_generico.py)**: Gerencia a importação de dados de arquivos JSON para o banco de dados. A função `importar_json_generico()` lê arquivos JSON do diretório configurado (`IMPORTS_DIR`), valida os dados e os insere no banco de dados. Logs detalhados são gerados para registrar sucessos e falhas.


- **Conexão com banco de dados: Oracle**: A conexão com o banco de dados Oracle é um ponto central do projeto e pode ser observada nos seguintes arquivos:

  - **[main.py](src/main.py)**: A função `main()` chama `iniciar_database()` para estabelecer a conexão inicial com o banco de dados e `check_or_create_tables()` para verificar ou criar as tabelas necessárias.
  - **[iniciar_database.py](src/database/login/iniciar_database.py)**: Contém a lógica para inicializar a conexão com o banco de dados Oracle, utilizando as credenciais fornecidas pelo usuário ou armazenadas em um arquivo codificado. A função `Database.init_oracledb()` é usada para estabelecer a conexão.
  - **[init_tables.py](src/database/models/init_tables.py)**: Verifica e cria as tabelas no banco de dados, chamando os métodos `check_or_create_table()` das classes de modelo.
  - **[model.py](src/database/tipos_base/model.py)**: Define a estrutura das tabelas e implementa métodos como `check_or_create_table()` e `save()` para interagir diretamente com o banco de dados Oracle, incluindo a criação, atualização e exclusão de registros.

  Esses arquivos trabalham em conjunto para garantir que a aplicação se conecte ao banco de dados Oracle e gerencie as tabelas e dados de forma eficiente.



## 🛠️ Problemas Solucionados

### 1️⃣ Estrutura Modular e Lógica Clara
O projeto segue uma **estrutura modular** bem organizada, com cada funcionalidade separada em arquivos e classes específicas. A lógica é clara e objetiva, com funções bem definidas para cada etapa, como:
- **Conexão ao banco de dados**.
- **Manipulação de dados** (cadastro, edição, exclusão, listagem).
- **Interação com o usuário**.

Essa abordagem facilita a **compreensão**, **manutenção** e **escalabilidade** do código.

---

### 2️⃣ Relevância aos Requisitos
O projeto atende diretamente aos requisitos solicitados, incluindo:
- **Conexão com o banco de dados Oracle**.
- **Manipulação de dados**: cadastro, edição, exclusão e listagem.
- **Exportação/Importação em JSON**.
- **Apresentação de relatórios**.

Todas as funcionalidades foram implementadas de forma alinhada ao objetivo principal: **criar um sistema de gestão eficiente para o agronegócio**.

---

### 3️⃣ Validação de Dados de Entrada
Para evitar inconsistências nos dados, o código utiliza funções específicas de validação, como:
- `input_int`
- `input_str`
- `input_bool`
- `input_enum`

Essas funções garantem que os dados inseridos pelo usuário sejam do tipo correto, evitando erros durante a gravação no banco de dados. Além disso:
- **Mensagens de erro claras** são exibidas em caso de entradas inválidas.

---

### 4️⃣ Apresentação Limpa e Usabilidade
Mesmo em um ambiente de linha de comando, o projeto prioriza a **boa usabilidade**:
- Utiliza a biblioteca **pandas** para exibir dados em formato tabular, tornando a apresentação mais organizada e fácil de entender.
- Mensagens informativas e logs guiam o usuário durante a interação com o sistema, proporcionando uma **experiência fluida e intuitiva**.
- Prints coloridos deixam a apresentação mais agradável e fácil de ler.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.
- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo de todas as fases.
  - <b>database</b>: Execução dos comandos de banco de dados, como Conectar, Cadastrar, Listar, Editar e Excluir. ([database](src/database/))
  - <b>file_exports</b>: Arquivos exportados do Bando de Dados no formato JSON. ([file_exports](src/file_exports/))
  - <b>file_imports</b>: Arquivos no formato JSON para importar no Banco de Dados. ([file_imports](src/file_imports/))
  - <b>logger</b>: Arquivos de formatação da aplicação. ([logger](src/logger/))
  - <b>menu</b>: Exibição e configuração de todos os menus da aplicação, como o da fazenda ([fazenda](src/menu/fazenda/)), insumos ([insumos](src/menu/insumos/)) e maquinário ([maquinario](src/menu/maquinario/)). <b>Obs:</b> a pasta generico compartilha funcionalidades padrões utilizadas por todos os menus. ([menu](src/menu/))
- <b>README</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

- Recomendamos utilizar o python versão 3.12.6 para executar o código.
- Para iniciar a aplicação é necessário instalar algumas bibliotecas, que são: (<b>arquivo: </b> [requirements.txt](requirements.txt))
  - oracledb==3.1.0*
  - pandas==2.2.3*
  - matplotlib==3.10.1
- Execute a função abaixo para instalar as bibliotecas (obs.: a instalação pode ocorrer de forma autamática a depender do seu ambiente):  
  - pip install -r requirements.txt
  <br> 
- Inicie a aplicação no [main.py](src/main.py):
- Informe o usuário do Banco de Dados (exemplo: RM000000) e logo em seguida informe a senha (exemplo: XXXXXX) e posteriormente o dsn. <b>Obs.:</b> caso não haja um usuário, senha e dsn válidos, não será possível seguir.
- Após a conexão com o Bando de Dados será exibido o menu da aplicação:
- <b><u>Importante:</u></b> Nessa etapa as tabelas FAZENDA, INSUMO e MAQUINARIO serão criadas no Banco de Dados para que os dados possam ser inseridos. A aplicação também verifica caso já tenham sido criadas antes.
1) Manutenção de Fazendas
2) Manutenção de Insumos
3) Manutenção de Maquinários
4) Relatórios
0) Sair

Opção 1: <b>Manutenção de Fazendas:</b> ([menu_fazenda.py](src/menu/fazenda/menu_fazenda.py))
1) Cadastrar Fazenda
2) Listar Fazendas
3) Editar Fazenda
4) Excluir Fazenda
5) Exportar Fazendas para JSON
6) Importar Fazendas de um JSON

* Aqui é possível gerenciar todos os dados da Fazenda, como Cadastrar, Listar, Editar, Excluir, além da Exportação ou Importação dos dados no formato JSON.

Opção 2: <b>Manutenção de Insumos:</b> ([menu_insumos.py](src/menu/insumos/menu_insumos.py))
1) Cadastrar Insumos
2) Listar Insumos
3) Editar Insumos
4) Excluir Insumos
5) Exportar Insumos para JSON
6) Importar Insumos de um JSON

* Aqui é possível gerenciar todos os dados dos Insumos, como Cadastrar, Listar, Editar, Excluir, além da Exportação ou Importação dos dados no formato JSON.

Opção 3: <b>Manutenção de Maquinário:</b> ([menu_maquinario.py](src/menu/maquinario/menu_maquinario.py))
1) Cadastrar Maquinário
2) Listar Maquinário
3) Editar Maquinário
4) Excluir Maquinário
5) Exportar Maquinário para JSON
6) Importar Maquinário de um JSON

* Aqui é possível gerenciar todos os dados do Maquinário, como Cadastrar, Listar, Editar, Excluir, além da Exportação ou Importação dos dados no formato JSON.

Opção 4: <b>Relatórios:</b> ([menu_relatorio.py](src/menu/relatorio/menu_relatorio.py))
1) Relatório de Fazendas
2) Relatório de Maquinários
3) Relatório de Insumos

* Em cada opção de relatório selecionada será exibido a lista de Fazendas, Maquinários ou Insumos cadastrados no Banco de Dados através das opções anteriores do Menu.

<strong>Exemplos de Relatórios:</strong>

- <strong>--- Relatório da Fazenda ---</strong>
- Nome: Joaozinho
- Tipo de Cultura: cana
- Formato: retangulo
- Base (m): 250.0
- Altura (m): 500.0
- Área (m²): 125000.0
  <br> 
- <strong>--- Relatório de Maquinário ---</strong>
- Fazenda: Joaozinho
- Maquinário: Colheitadeira
- Área da fazenda (m²): 125000.0
- Formato da fazenda: Retângulo
- Largura do equipamento (m): 4.0
- Velocidade máxima (km/h): 10.0
- Distância total (km): 3907.24
- Eficiência (km/l): 20.0
- Consumo estimado (litros): 195.36
- Tempo estimado: 558h 10min
- Número de voltas: 125
- Rota gerada: Ver arquivo Rota_Colheitadeira_Joaozinho_*.png (aqui é gerado uma imagem com o desenho da rota realizada pelo maquinário, o arquivo é disponibillizado na pasta [file_exports](src/file_exports/).)
  <br> 
- <strong>--- Relatório de Insumos ---</strong>
- Fazenda: Joaozinho
- Insumo: Fosforo
- Tipo de Cultura: cana
- Área total (hectares): 12.5
- Unidade de medida: kg
- Consumo por hectare: 50.0 kg/ha
- Consumo total estimado: 625.0
- Custo por unidade: R$150.0/kg
- Custo total estimado: R$93750.0
- Detalhes: Equivalente a 625.0 kg



## 🗃 Histórico de lançamentos

* 0.1.3 - 21/04/2025  - Atualização do readme para a inclusão das informações sobre os relatórios.
* 0.1.2 - 18/04/2025  - Inclusão dos relatórios na aplicação.
* 0.1.1 - 17/04/2025  - Atualização do readme para a inclusão de informações sobre o projeto e melhorias na formatação do código.
* 0.1.0 - 15/04/2025  - Versão preliminar da nossa aplicação que inclui a geração do script de Banco de Dados

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


