import os
import yaml

def yaml_to_env(yaml_text):
    config = yaml.safe_load(yaml_text)
    env_text = ""

    def convert_to_env(config, prefix=""):
        nonlocal env_text
        
        for key, value in config.items():
            if isinstance(value, dict):
                convert_to_env(value, prefix + key + ".")
            else:
                env_variable = prefix + key
                env_text += f"{env_variable}={value}\n"

    convert_to_env(config)
    return env_text


def env_to_yaml(env_text):
    config = {}

    for line in env_text.splitlines():
        if "=" in line:
            env_variable, value = line.split("=")
            keys = env_variable.split(".")
            current_dict = config

            for key in keys[:-1]:
                if key not in current_dict:
                    current_dict[key] = {}
                try:
                    current_dict = float(current_dict[key])
                except:
                    try:
                        if current_dict[key].lower() == 'true':
                            current_dict = True
                        if  current_dict[key].lower() == 'false':
                            current_dict = False
                    except:
                        current_dict = current_dict[key]


            try:
                current_dict[keys[-1]] = float(value)
            except:
                if value.lower() == 'true':
                    current_dict[keys[-1]] = True
                elif  value.lower() == 'false':
                    current_dict[keys[-1]] = False
                else: 
                    current_dict[keys[-1]] = value

    return yaml.dump(config)
