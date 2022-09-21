
[Read it in english here!](README.md)

![law jolly roger](https://static.wikia.nocookie.net/onepiece/images/7/76/Heart_Pirates%27_Jolly_Roger.png/revision/latest?cb=20140715211602)

# 🏴‍☠️ Trafalgar Log
Trafalgar Log é um Framework Python que padroniza JSON Logs e simplifica a 
forma de usá-lo. Seu objetivo principal é abstrair a implementação de logs 
para ferramentas que realizam o parse de dados em formato JSON em eventos 
de logs, como o Splunk, Kibana, CloudWatch Logs, etc.
Esse framework foi construído usando como base os pacotes [logging](https://docs.python.org/3/library/logging.html) and [python-json-logger](https://pypi.org/project/python-json-logger/).

## 🧬 Estrutura do log
Abaixo está uma seção detalhada sobre cada campo logado quando você usa a Trafalgar Log:

| Responsável | Nome do campo      | Descrição                                                                                                                                                                                           |
|:-----------:|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      ✍      | **app**            | Representa o nome da aplicação que gerou o evento de log.                                                                                                                                           |
|     🍕      | **flow**           | Esse campo deve ser usado como um identificador de quem estimulou a aplicação para iniciar a execução que está sendo logada.                                                                        |
|    🐻‍❄     | **code_line**      | Linha do código onde ocorreu o evento de log.                                                                                                                                                       |
|     🍕      | **correlation_id** | ID usado para rastrear uma única execução, do começo ao fim.                                                                                                                                        |
|    🐻‍❄     | **date_time**      | Data e hora do evento do log no formato yyyy-MM-dd hh:mm:ss.SSS - exemplo: 2022-09-18 19:25:43.749                                                                                                  |
|      ✍      | **domain**         | Domínio da aplicação que pode ser usado para representar o domínio funcional da aplicação.                                                                                                          |
|     🍕      | **instance_id**    | ID usado para representar a instância da aplicação; pode ser um endereço IP, o ID de uma instância de função Lambda, etc.                                                                           |
|     💻      | **log_code**       | Uma String que representa um propósito geral do evento do log; pode ser usado para representar todos os logs de operações com bancos de dados, por exemplo.                                         |
|     💻      | **log_message**    | A mensagem de log que você quer gerar.                                                                                                                                                              |
|     💻      | **payload**        | Esse campo pode ser, literalmente, qualquer coisa; se for um tipo primitivo, será logado como ele é, mas se for um objeto complexo, uma lista ou até um dicionário, será logado com um objeto JSON. |
|    🐻‍❄     | **severity**       | O nível do log do evento de log.                                                                                                                                                                    |
|    🐻‍❄     | **timestamp**      | Timestamp do evento de log em milisegundos.                                                                                                                                                         |

### Legenda da tabela

| Legenda | Descrição                                                                                                                 |
|:-------:|:--------------------------------------------------------------------------------------------------------------------------|
|   ✍️    | Você é responsável por configurar esse campo através de <br/>variáveis de ambiente ([veja seção](#variáveis-de-ambiente)) |
|  🐻‍❄️  | Esse campo é preenchido automaticamente a cada evento de log.                                                             |
|   💻    | Quando você codifica um evento de log, passe esse campo para o método de log ([veja seção](#logando-eventos))             |
|   🍕    | Esse campo é opcional, mas faz com que seu log fique mais fácil de ser analisado ([veja seção](#campos-opcionais))        |


## ⚙️ Configuração
### Variáveis de ambiente
Para o Trafalgar Log funcionar na sua aplicação, você precisa adicionar 
essas variáveis de ambiente:
- **TRA_LOG_APP_NAME (obrigatório):** Essa é a variável de ambiente que 
  será usada no campo **app** no evento de log.
- **TRA_LOG_DOMAIN (obrigatório):** Essa é a variável de ambiente que 
  será usada no campo **domain** no evento de log.
- **TRA_LOG_LEVEL (opcional):** Essa variável será usada para atributo [o nível do log](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel); 
  os valores aceitos para essa variável são:
  - INFO
  - DEBUG
  - WARNING
  - ERROR
  - CRITICAL
  - NOTSET
  Para mais informações, visite [Logging Levels](https://docs.python.org/3/library/logging.html#levels).
- **TRA_LOG_FIELDS_TO_MASK (opcional):** Se a sua aplicação possui dados 
  sensíveis sendo logados, você pode querer listar todos os campos que 
  guardam esses dados sensíveis e colocá-los nessa variável. Por exemplo, 
  se a sua aplicação loga o documento de uma pessoa e o evento de log 
  possui um campo chamado "CPF" e outro campo chamado "senha", você pode 
  mascarar o conteúdo desses campos atribuindo um valor a essa 
  variável de ambiente da seguinte forma: TRA_LOG_FIELDS_TO_MASK="cpf,senha". 
  O evento de log será logado dessa forma:
  ```json
  {
    "app": "readme-docs",
    "flow": "escrevendo a documentação",
    "code_line": "main.py - <module>:29",
    "correlation_id": "552f5139-5da9-4e89-8c1b-9d2a81f9461c",
    "date_time": "2022-09-18 19:25:43.749",
    "domain": "victoraugustofd",
    "instance_id": "347f2d8d-0bde-485e-a120-513e972a3cee",
    "log_code": "Banco de dados",
    "log_message": "Buscando dados do contribuidor no banco de dados.",
    "payload": {
      "cpf": "*",
      "senha": "*",
      "nome_contribuidor": "Trafalgar Law"
    },
    "severity": "INFO",
    "timestamp": 1663539943749
  }
  ```
  Trafalgar Log já possui alguns campos que são sempre mascarados, como 
  "password", "senha" and "contraseña".

### Logando eventos

Abaixo estão alguns exemplos de todos os tipos de logs que o Trafalgar Log 
pode logar (isso é apenas um bloco de código apenas para exemplificar 
como usar este pacote):

```python
from trafalgar_log.core.logger import Logger
from docs.out.adapters import DatabaseAdapter
from docs.core.exceptions import DocsBusinessError
from typing import Optional

database_port = DatabaseAdapter()


def get_contributor_data(contributor_id: str) -> Optional[dict]:
  try:
    Logger.info(log_code="Banco de dados",
                log_message="Buscando dados do contribuidor no banco de dados.",
                payload=f"ID do contribuidor: {contributor_id}")
    contributor_data = database_port.get_contributor_data(contributor_id)

    # É opcional nomear os argumentos, desde que a ordem log_code, 
    # log_message e payload seja respeitada.
    Logger.info("Banco de dados", "Contribuidor encontrado no banco de dados.", contributor_data)

    if contributor_data.get("test_field"):
      Logger.debug("Banco de dados", "Debugando método.", contributor_data.get("test_field"))

    if contributor_data.get("status") != "ACTIVE":
      Logger.warn("Banco de dados", "Contribuidor não está ativo.", contributor_data.get("status"))

    return contributor_data
  except DocsBusinessError as business_error:
    Logger.error("Banco de dados", f"Erro ao buscar os dados do contribuidor: {str(business_error)}", f"ID do contribuidor: {contributor_id}")
  except Exception as exception:
    Logger.critical("Banco de dados", f"Exceção ao buscar os dados do contribuidor: {str(exception)}", f"ID do contribuidor: {contributor_id}")
  finally:
    return None
```

### Campos opcionais
Os três campos opcionais abaixo devem ser atribuídos no início do processo, 
para que todos os logs subsequentes compartilhem os mesmos dados.

- **correlation_id**: Esse campo deve ser preenchido com um correlation_id 
  já predefinido que alguém passou para a aplicação. Se esse campo não for 
  configurado no início da execução, o Trafalgar Log irá gerar um com o método 
  uuid.uuid4().
  
  **Implementação**:
  ```python
  from trafalgar_log.core.logger import Logger

  Logger.set_correlation_id("coloque aqui o correlation_id recebido ou crie um")
  ```
- **flow:** Se não for configurado, o Trafalgar Log irá atribuir o valor NOT_SET a 
  este campo.

  **Implementação**:
  ```python
  from trafalgar_log.core.logger import Logger

  Logger.set_flow("coloque aqui o flow desejado")
  ```
- **instance_id:** Se não for configurado, o Trafalgar Log irá atribuir o valor NOT_SET a 
  este campo.

  **Implementação**:
  ```python
  from trafalgar_log.core.logger import Logger

  Logger.set_instance_id("put here the desired instance_id")
  ```

## Logando exceções
Toda vez que você quiser logar uma exceção, você deve usar o método 
Logger.error() ou Logger.critical() por dois motivos:
1. Boas práticas
2. Trafalgar Log está preparado para capturar o stacktrace da exceção com esses 
   dois métodos e logá-lo como um array de strings, como o exemplo abaixo:
  ```json
  {
    "app": "readme-docs",
    "flow": "escrevendo a documentação",
    "code_line": "main.py - <module>:34",
    "correlation_id": "545723a8-1ed8-4886-80d6-9fdb7250351e",
    "date_time": "2022-09-20 23:03:15.976",
    "domain": "victoraugustofd",
    "instance_id": "417f06d6-06ce-47a6-9151-86afb93c3265",
    "log_code": "Gerando exceção",
    "log_message": "Tentando recuperar uma chave inválida em um dicionário.",
    "payload": "",
    "severity": "ERROR",
    "timestamp": 1663725795976,
    "stacktrace": [
        "Traceback (most recent call last):",
        "  File \"D:\\Documents\\Victor\\Git\\GitHub\\victoraugustofd\\trafalgar-log\\main.py\", line 32, in <module>",
        "    os.environ[\"a\"]",
        "  File \"D:\\Program Files\\Python\\lib\\os.py\", line 679, in __getitem__",
        "    raise KeyError(key) from None",
        "KeyError: 'a'"
    ]
  }
  ```
