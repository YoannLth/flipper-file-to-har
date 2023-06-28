import json
import sys

# script that prints the structure of a JSON file. Used to understand the structure of Flipper export files
def print_json_structure(data, indent=0, output_file=sys.stdout):
    if isinstance(data, dict):
        for key, value in data.items():
            value_type = type(value).__name__
            print(f"{' ' * indent}{key}: {value_type}", file=output_file)
            print_json_structure(value, indent + 2, output_file)
    elif isinstance(data, list):
        for item in data:
            item_type = type(item).__name__
            print(f"{' ' * indent}- {item_type}", file=output_file)
            print_json_structure(item, indent + 2, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python myScript.py input.json output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        json_data = json.load(file)

    with open(output_file, 'w') as output:
        print_json_structure(json_data, output_file=output)
