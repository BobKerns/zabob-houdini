import re

# Read the file
with open('src/zabob_houdini/houdini_test_functions.py', 'r') as f:
    content = f.read()

# Define the functions we need to convert
functions_to_convert = [
    'test_chain_copy',
    'test_chain_copy_deep_nodes', 
    'test_chain_copy_nested',
    'test_chain_flatten_memoization',
    'test_chain_flatten_nested',
    'test_node_copy_non_chain_inputs',
    'test_node_instance_copy',
    'test_node_instance_copy_with_inputs',
    'test_node_registry'
]

# Pattern to match function with try/except/json.dumps
pattern = r'(def (test_[^(]+)\([^)]*\):\s*\n\s*"""[^"]*"""\s*\n)\s*try:\s*\n(.*?)\s*return json\.dumps\(([^)]+)\)\s*\n\s*except Exception as e:\s*\n\s*error_result = \{\s*\'success\': False,\s*\'error\': str\(e\),\s*\'traceback\': traceback\.format_exc\(\)\s*\}\s*return json\.dumps\(error_result\)'

def convert_function(match):
    func_header = match.group(1)
    func_name = match.group(2)
    func_body = match.group(3)
    result_var = match.group(4)
    
    if func_name not in functions_to_convert:
        return match.group(0)  # Don't convert
    
    # Add decorator and return type
    new_header = func_header.replace(f'def {func_name}(', f'@houdini_result\ndef {func_name}(')
    if ') -> JsonObject:' not in new_header:
        new_header = new_header.replace('):', ') -> JsonObject:')
    
    # Remove extra indentation and add proper return
    body_lines = func_body.split('\n')
    cleaned_body = []
    for line in body_lines:
        if line.strip():
            cleaned_body.append(line[4:] if line.startswith('    ') else line)  # Remove 4 spaces of indentation
    
    new_func = f'{new_header}    {"".join([line + "\n" for line in cleaned_body])}    return cast(JsonObject, {result_var})'
    
    return new_func

# Apply conversion
new_content = re.sub(pattern, convert_function, content, flags=re.DOTALL)

print("Conversion completed - writing to file")

# Write back
with open('src/zabob_houdini/houdini_test_functions.py', 'w') as f:
    f.write(new_content)

print("File updated")
