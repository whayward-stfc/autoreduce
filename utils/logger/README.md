## log_decorator.py
The log class decorator can be used similarly to the log handler. The log decorator is a decorator 
to place on methods which you wish to log.

### Parameters & Usage:

```python
@LogDecorator(logger, log_level, log_file_name, stream_log)
```

* logger:
    * Logger object
* log_leveL:
    * Description: The level to log at
    * Type: string
    * Default value: None
* log_file_name:
    * Description: Name of log file
    * Type: string
    * Default value: None
* stream_log:
    * Description: Toggle streaming of logs to CLI
    * Type: Bool (True, False)
    * Default value: None

Basic Usage
```python
from utils.logger.log_decorator import LogDecorator
from utils.logger.log_handler import GetLogger

logger = GetLogger()

@LogDecorator(logger=logger, stream_log=True)
def func(a, b, c):
    answer = a + b + c
    return answer
```
