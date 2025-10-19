import yaml
from pprint import pprint

from ._blpath import package_path

with (package_path() / "schema.yaml").open("r") as f:
    schema = yaml.safe_load(f)

def print_schema(as_yaml=True):
    if as_yaml:
        print(yaml.dump(schema))
    else:
        pprint(schema)
