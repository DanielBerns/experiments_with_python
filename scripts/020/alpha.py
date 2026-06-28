import yaml
import pprint

# Define the path to your YAML file
file_path = './scripts/020/config.yaml'


def read_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            # Use safe_load to securely parse the YAML file
            config_data = yaml.safe_load(file)

            print("Successfully loaded configuration:\n")
            # pprint makes nested lists and dictionaries much easier to read
            pprint.pprint(config_data, sort_dicts=False)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except yaml.YAMLError as error:
        print(f"Error parsing YAML file: {error}")

if __name__ == "__main__":
    read_yaml(file_path)
