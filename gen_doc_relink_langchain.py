import json
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

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

def create_openai_client(api_key, api_base):
    openai.api_key = api_key
    openai.api_base = api_base

def generate_class_documentation(class_data):
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

# Tokenize and store documentation in vector space using LangChain
def tokenize_and_store_documentation(documentation, api_key, api_base):
    # Tokenize the documentation
    splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(documentation)
    
    # Wrap chunks into Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(api_key=api_key, api_base=api_base)
    
    # Store in vector space
    vector_store = FAISS.from_documents(documents, embeddings)
    
    return vector_store

def add_new_feature_prompt(vector_store, api_key, api_base, feature_description):
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["feature_description"],
        template="Given the following documentation, suggest code to add the feature: {feature_description}",
    )
    
    # Create a LangChain with OpenAI
    llm_chain = LLMChain(llm=openai.Completion(api_key=api_key, api_base=api_base), prompt_template=prompt_template)
    
    # Query the vector store and generate new feature code
    query_results = vector_store.query(feature_description)
    response = llm_chain.run({"feature_description": feature_description, "documentation": query_results})
    
    return response

# Generate yUML text
yuml_text = generate_yuml(class_data)

# Set your API key and base URL
api_key = "your_custom_api_key"
api_base = "https://your-custom-api-base-url/v1"

# Optionally, generate documentation using OpenAI
create_openai_client(api_key, api_base)

documentation = generate_class_documentation(class_data)
print("Generated yUML text:")
print(yuml_text)
print("\nGenerated Documentation:")
print(documentation)

# Tokenize and store documentation in vector space
vector_store = tokenize_and_store_documentation(documentation, api_key, api_base)

# Example of adding a new feature
feature_description = "Add a new method to calculate the sum of two integers."
new_feature_code = add_new_feature_prompt(vector_store, api_key, api_base, feature_description)
print("\nNew Feature Code:")
print(new_feature_code)
