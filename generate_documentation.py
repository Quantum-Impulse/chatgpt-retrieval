import json
import openai

# Load JSON data
with open('ClassTree.json', 'r') as file:
    class_data = json.load(file)

def generate_yuml(class_data):
    yuml_lines = []
    for class_name, class_info in class_data.items():
        # Check for inheritance
        for parent_class in class_info.get("extends", []):
            yuml_lines.append(f"[{parent_class}]^- [{class_name}]")
    return "\n".join(yuml_lines)

def create_openai_client(api_key):
    openai.api_key = api_key

def generate_class_documentation(class_data, openai_client):
    documentation = []
    for class_name, class_info in class_data.items():
        doc = f"Class: {class_name}\n"
        doc += f"Kind: {class_info.get('kind')}\n"
        doc += "Methods:\n"
        for method in class_info.get("methods", []):
            doc += f"  {method.get('name')}({method.get('parameters')}) : {method.get('return type')}\n"
        doc += "\n"
        documentation.append(doc)
    
    return "\n".join(documentation)

# Generate yUML text
yuml_text = generate_yuml(class_data)

# Optionally, generate documentation using OpenAI
api_key = "your_openai_api_key_here"
create_openai_client(api_key)

documentation = generate_class_documentation(class_data, openai)
print("Generated yUML text:")
print(yuml_text)
print("\nGenerated Documentation:")
print(documentation)
