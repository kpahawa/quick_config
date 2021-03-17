# QuickConfig
<hr>

## Description
QuickConfig is a super lightweight dynamic config provider for python applications. 
The config provider uses a runtime config that can be imported to any part of your 
application. The provider allows you to use runtime environment variables and configs 
anywhere in your application via a simple import.

### Design
The quick config provider relies on a standard structure for an application's 
configurations. All configurations must be provided in a standard `config` directory. 
Configs in the `config` directory must follow the standard deployment configuration
names like `staging.py` or `test.py` or `production.py`. Once the runtime environment
is set via an environment variable `environment`, the config provider will read
that and populate the configs available to the entire application as methods.

### Usage
1. Create an application like a Django/Flask Application which has runtime configs which may
   differ for each run time environment using the following nomenclature:
   - create a directory called `config`
    - create files in the directory with the following structure
   ```python
   # config/base.py:
   import os
   
   ENV_VARS = {
       "some_api_key": os.environ.get('my_api_key'),
        "db_name": "my_default_db",
        "important_array": ['a', 'b', 'c', 'd']
   }
   ```
   ```python
   # config/production.py:
   import os
   
   ENV_VARS = {
        "db_name": os.environ.get("production_db"),   # overwrites base.py
        "important_array": [1, 2, 3, 4]  # overwrites base.py
   }
   ```
   ```python
   # config/development.py: 
   ENV_VARS = {
        "db_name": "my_dev_db",
   }
   ```
   - Note the use of `ENV_VARS` in each environment file. That is required
2. Install the qc config `pip install qc`
3. Use the environment vars in your application directly:
```python
# in my_app/my_module/file.py
from qc import config

class MyModule:    
    def __init__(self):
        self.logger = config.get_logger()
        self.api_key = config.some_api_key()
        
        # depending on environment, this will change
        self.important_index_value = config.important_array(0)

global_db_name = config.db_name()

```
