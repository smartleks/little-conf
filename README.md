# little-conf


## Project description

Simple app configuration utility

- 100% Pydantic config style
- Different app environments (local/dev/prod etc.)
- Use yaml files and/or environment variables
- Dynamic reload config on SIGHUP


## Install

`pip install little-conf`


## Custom configuration options

```python

class Config(LittleConfig):
    var1: int  # get from config file
    var2: str = ''

    class Config:
        yaml_conf_path = 'config'  # path to directory with config (default 'config')
        env_prefix = 'env_prefix'  # name of env variable with prefix for all services environment variables (default name: `env_prefix`, default value: `service_`)
        env = 'service_env'        # name of env variable with app environment (default name `service_env`, defaulr value: `local`)
 
```

## Usage Examples

- [simple_app](examples/simple_app.py)
- [example_reload_on_sighup](examples/example_reload_on_sighup.py)
