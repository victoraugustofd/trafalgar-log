
![law jolly roger](https://onepiece.fandom.com/wiki/Heart_Pirates?
file=Heart_Pirates%2527_Jolly_Roger.png)

# 🏴‍☠️ Trafalgar Log
Trafalgar Log is a Python Framework that standardize JSON Logs and make it 
easy to use. Its main goal is to abstract log implementation for tools that 
parse JSON data in log events, such as Splunk, Kibana, CloudWatch Logs, etc.
This framework was built on top of the packages [logging](https://docs.python.org/3/library/logging.html) and 
[python-json-logger](https://pypi.org/project/python-json-logger/).

## 🧬 Log Structure
Below is a detailed section about each field printed when you use Trafalgar 
Log:

| Responsible | Field name         | Description                                                                                                                                                                        |
|:-----------:|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      ✍      | **app**            | Represents the application name that generated the log event                                                                                                                       |
|     🍕      | **flow**           | This field should be used as an identifier of who estimulated the application to start the execution which is being logged.                                                        |
|    🐻‍❄     | **code_line**      | Code line that the log event occurred                                                                                                                                              |
|     🍕      | **correlation_id** | ID used to trace a single execution, end-to-end.                                                                                                                                   |
|    🐻‍❄     | **date_time**      | Datetime of the log event on the format yyyy-MM-dd hh:mm:ss.S - e.g., 2022-09-18 19:25:43.749                                                                                      |
|      ✍      | **domain**         | Application domain that can be used to represent the functional domain of the application.                                                                                         |
|     🍕      | **instance_id**    | ID used to represent the application instance; it can be an IP Address, an ID of a lambda funcion instance, etc.                                                                   |
|     💻      | **log_code**       | A String that represents a general purpose of the log event; it can be used to represent all logs of a database, for example.                                                      |
|     💻      | **log_message**    | The log message that you want to print                                                                                                                                             |
|     💻      | **payload**        | This can be literally anything; if it is a primitive type, it will be printed as it is, but if it is a complex object, a list or even a dict, it will be printed as a JSON object. |
|    🐻‍❄     | **severity**       | The log level of the log event.                                                                                                                                                    |
|    🐻‍❄     | **timestamp**      | Timestamp of the log event in miliseconds.                                                                                                                                         |

### Table legend

| Legend | Description                                                                                                        |
|:------:|:-------------------------------------------------------------------------------------------------------------------|
|   ✍️   | You are responsible for configuring this field through environment variable ([see section](#environment-variables) |
| 🐻‍❄️  | This field is automatically filled in each log event.                                                              |
|   💻   | When you code your log event, you will need to pass this field to log method ([see section](#logging-events))      |
|   🍕   | This field is optional, but makes your log easier to analyse ([see section](#optional-fields))                     |


## ⚙️ Configuration
### Environment variables
For Trafalgar Log work in your application, you need to add these 
environment variables:
- **TRA_LOG_APP_NAME (mandatory):** This is the environment variable that 
  will be used as the **app** field in the log event.
- **TRA_LOG_DOMAIN (mandatory):** This is the environment variable that will be used 
  as the **domain** field in the log event.
- **TRA_LOG_LEVEL (optional):** This will be used to set [the log level for the logging](https://docs.python.org/3/library/logging.html#logging.Logger.
  setLevel); the accepted values for this variable are as follows:
  - INFO
  - DEBUG
  - WARNING
  - ERROR
  - CRITICAL
  - NOTSET
  For more information, please visit [Logging Levels](https://docs.python.org/3/library/logging.html#levels).
- **TRA_LOG_FIELDS_TO_MASK (optional):** If your application has sensitive 
  data being logged, you might want to list all fields that holds these sensitive data 
  and set this variable with them. For example, if your application logs a 
  brazilian document ID (CPF) and a log event have a field called "CPF" and 
  another field called "password", you can mask its content by setting your 
  environment variable like this: TRA_LOG_FIELDS_TO_MASK="cpf,password". 
  The log event will be printed like this:
  ```json
  {
    "app": "readme-docs",
    "flow": "writing documentation",
    "code_line": "main.py - <module>:29",
    "correlation_id": "552f5139-5da9-4e89-8c1b-9d2a81f9461c",
    "date_time": "2022-09-18 19:25:43.749",
    "domain": "victoraugustofd",
    "instance_id": "347f2d8d-0bde-485e-a120-513e972a3cee",
    "log_code": "Contributor data",
    "log_message": "Getting contributor data from database.",
    "payload": {
      "cpf": "*",
      "password": "*",
      "contributor_name": "Trafalgar Law"
    },
    "severity": "INFO",
    "timestamp": 1663539943749
  }
  ```
  Trafalgar Log already has some fields that are always ommited, such as 
  "password", "senha" and "contraseña".

### Logging events

Here are some examples of all types os logs that Trafalgar Log can print 
(this is just a code snippet only to exemplify how to use this package):

```python
from trafalgar_log.core.logger import Logger
from docs.out.adapters import DatabaseAdapter
from docs.core.exceptions import DocsBusinessError
from typing import Optional

database_port = DatabaseAdapter()


def get_contributor_data(contributor_id: str) -> Optional[dict]:
  try:
    Logger.info(log_code="Contributor data",
                log_message="Getting contributor data from database.",
                payload=f"Contributor id: {contributor_id}")
    contributor_data = database_port.get_contributor_data(contributor_id)

    # It is optional to name the arguments, since the order log_code, 
    # log_message and paylod are respected.
    Logger.info("Contributor data", "Contributor found on database.", contributor_data)

    if contributor_data.get("test_field"):
      Logger.debug("Contributor data", "Debugging method.", contributor_data.get("test_field"))

    if contributor_data.get("status") != "ACTIVE":
      Logger.warn("Contributor data", "Contributor not active.", contributor_data.get("status"))

    return contributor_data
  except DocsBusinessError as e:
    Logger.error("Contributor data", f"Error getting contributor data: {str(e)}", f"Contributor id: {contributor_id}")
  except Exception as e:
    Logger.critical("Contributor data", f"Exception getting contributor data: {str(e)}", f"Contributor id: {contributor_id}")
  finally:
    return None
```

### Optional fields
The three optional fields below should be set at the beginning of the 
process, so all subsequent log events share the same data.

- **correlation_id**: This field should be filled with an already 
  predefined correlation_id that someone passed to the application. If this 
  is not set at the beginning of the execution, the package will generate 
  one with uuid.uuid4().
  
  **Implementation**:
  ```python
  from trafalgar_log.core.logger import Logger

  Logger.set_correlation_id("put here the correlation_id received or create one")
  ```
- **flow:** If not set, the package will set this field as NOT_SET.

  **Implementation**:
  ```python
  from trafalgar_log.core.logger import Logger

  Logger.set_flow("put here the desired flow")
  ```
- **instance_id:** If not set, the package will set this field as NOT_SET.

  **Implementation**:
  ```python
  from trafalgar_log.core.logger import Logger

  # This line should be at the beginning of the execution, so all the 
  # subsequent log events share the same correlation_id for tracing purposes.
  Logger.set_instance_id("put here the desired instance_id")
  ```

## Exception logging
Every time that you want to log an exception, you should use the method 
Logger.error() or Logger.critical() for two reasons:
1. Convention
2. The package is prepared to capture the stacktrace of the exception with 
   this two methods and print as an array of strings, as in the example below:
  ```json
  {
    "app": "readme-docs",
    "flow": "writing documentation",
    "code_line": "main.py - <module>:34",
    "correlation_id": "545723a8-1ed8-4886-80d6-9fdb7250351e",
    "date_time": "2022-09-20 23:03:15.976",
    "domain": "victoraugustofd",
    "instance_id": "417f06d6-06ce-47a6-9151-86afb93c3265",
    "log_code": "Generating exception",
    "log_message": "Trying to get an invalid key from a dict.",
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
