import yaml
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "config.yaml"
abs_file_path = os.path.join(script_dir, rel_path)
params = yaml.full_load(open(abs_file_path))

