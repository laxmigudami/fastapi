import os
import json
import pathlib
from utils.openai import get_openai_response
import copy
from dotenv import load_dotenv
import re
import hashlib

load_dotenv()
BASE_URL = os.getenv("BASE_URL_APP")

def resolve_ref(ref, root):
    if not ref.startswith('#/'):
        return None
    parts = ref[2:].split('/')
    result = root
    for part in parts:
        result = result.get(part)
        if result is None:
            return None
    if '$ref' in result:
        return resolve_ref(result['$ref'], root)
    if 'properties' in result:
        for key, prop in result['properties'].items():
            if '$ref' in prop:
                result['properties'][key] = resolve_ref(prop['$ref'], root)
    if result.get('type') == 'array' and '$ref' in result.get('items', {}):
        result['items'] = resolve_ref(result['items']['$ref'], root)
    return result

def expand_refs_in_operation(operation, root):
    op = copy.deepcopy(operation)
    def resolve_schema(schema):
        if schema and '$ref' in schema:
            return resolve_ref(schema['$ref'], root)
        if schema and schema.get('type') == 'array' and '$ref' in schema.get('items', {}):
            schema['items'] = resolve_ref(schema['items']['$ref'], root)
        return schema
    if op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema'):
        op['requestBody']['content']['application/json']['schema'] = \
            resolve_schema(op['requestBody']['content']['application/json']['schema'])
    if op.get('responses'):
        for code, resp in op['responses'].items():
            if resp.get('content', {}).get('application/json', {}).get('schema'):
                resp['content']['application/json']['schema'] = \
                    resolve_schema(resp['content']['application/json']['schema'])
    # Added this print to inspect the expanded operation
    print("Expanded operation:", json.dumps(op, indent=2))
    return op

def generate_pytest_prompt(path, method, operation):
    return f"""
You are a Python developer. Generate pytest tests for API testing for the app using the requests library.

Requirements:
- Output ONLY valid Python code. DO NOT include any comments, explanations, markdown formatting, or introductory text.
- Do NOT add any header comments, docstrings, or import statements for fixtures, database, or conftest.py.
- Assume all required fixtures (client, authorized_client, test_user, test_user2, test_posts, token) are available from conftest.py and do NOT import them.
- Only import models or schemas if needed for validation(such as from app import models and from app import schemas).
- access token will be generated using the token fixture. and also which will be used under authorized_client fixture.
- Do not define any fixtures in the test files unless absolutely necessary.
- Output only valid, runnable Python pytest code for your project structure.
- Group all tests for the resource in a single file.
- Use pytest fixtures (client, authorized_client, test_user, test_user2, test_posts, token) as function arguments based on the requirements for the test function, do NOT import them as Conftest.py is already set up with these fixtures.
- For authentication, use the authorized_client fixture for requests that require authentication.
- Use @pytest.mark.parametrize for multiple scenarios and edge cases.
- Validate response data using schemas from FASTAPI/app/schemas.py, e.g., schemas.PostOut(**res.json()).
- Assert both status code and response content depends on the HTTP Method.
- For LOGIN tests, validate JWT tokens using the secret key and algorithm from app/config.py. And Generate tests for create user and login operations(Valid and Invalid).
- Cover all CRUD operations for the resource, including:
    - GET all
    - GET by ID (existing, non-existent, unauthorized)
    - POST (valid, invalid, missing fields, wrong types)
    - PUT (valid, invalid, unauthorized, non-existent)
    - DELETE (authorized, unauthorized, non-existent)
- For authentication, test:
    - Requests with valid authentication (should succeed)
    - Requests without authentication (should fail with 401)
    - Requests with invalid authentication (should fail with 401 or 403)
- For negative tests, include:
    - Invalid IDs (string, float, negative, zero)
    - Missing required fields
    - Empty strings
    - Wrong types
    - Non-existent resources
- Use realistic database setup and teardown via client fixture implemented in the tests/conftest.py.
- Assert on both status code and response body, including error details.
- Only check response.json() if the OpenAPI response schema specifies a JSON body.
- For DELETE requests, do not assert on response.json() unless a response body is defined in the OpenAPI spec.
- When testing GET/PUT/DELETE for a specific resource by ID, first create the resource with a POST request (if possible), then use its ID for the test.
- Output only valid, runnable Python pytest code.

OpenAPI operation:
{json.dumps(operation, indent=2)}
"""

def sanitize_filename(method, path_key):
    segments = [s for s in path_key.split('/') if s]
    entity = 'endpoint'
    for seg in reversed(segments):
        if not (seg.startswith('{') and seg.endswith('}')):
            entity = seg
            break
    entity = entity.capitalize()
    return f"test_{method.lower()}_{entity.lower()}.py"

def clean_ai_response(code):
    # Remove header comments and markdown
    code = re.sub(r"^#.*\n", "", code)
    code = re.sub(r"^\"\"\".*?\"\"\"\n", "", code, flags=re.DOTALL)
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)
    code = re.sub(r"^Here is the pytest code.*\n?", "", code, flags=re.IGNORECASE)
    code = re.sub(r"^.*pytest code.*requests library.*\n?", "", code, flags=re.IGNORECASE)
    code = re.sub(r"^This code covers*", "", code, flags=re.DOTALL)
    return code.strip()

def generate_pytest_tests_via_ai(spec_file, tests_dir):
    with open(spec_file, encoding="utf-8") as f:
        parsed_spec = json.load(f)
    paths = parsed_spec.get("paths", {})
    print("Generating pytest tests for the following paths:")
    print(paths)

    pathlib.Path(tests_dir).mkdir(parents=True, exist_ok=True)

    resource_groups = group_operations_by_resource(paths)

    for resource, operations in resource_groups.items():
        prompt = ""
        op_list = []
        for path_key, method, operation in operations:
            op_expanded = expand_refs_in_operation(operation, root=parsed_spec)
            prompt += generate_pytest_prompt(path_key, method, op_expanded) + "\n"
            op_list.append(op_expanded)
        test_hash = get_test_hash(prompt, op_list)
        file_name = f"test_{resource}.py"
        out_path = os.path.join(tests_dir, file_name)
        if not is_test_up_to_date(out_path, test_hash):
            response = get_openai_response(prompt)
            code = response if isinstance(response, str) else getattr(response, "content", "")
            cleaned = clean_ai_response(code)
            write_test_with_hash(out_path, cleaned, test_hash)
            print(f"Generated/updated pytest: {file_name}")
        else:
            print(f"Skipped (up-to-date): {file_name}")

def get_test_hash(prompt, operation):
    hash_input = prompt + json.dumps(operation, sort_keys=True)
    return hashlib.md5(hash_input.encode("utf-8")).hexdigest()

def write_test_with_hash(out_path, code, test_hash):
    # Save the test file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)
    # Save the .meta file in a separate directory
    meta_dir = os.path.join(os.path.dirname(out_path), ".meta")
    os.makedirs(meta_dir, exist_ok=True)
    meta_path = os.path.join(meta_dir, os.path.basename(out_path) + ".meta")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(test_hash)

def is_test_up_to_date(test_path, hash_value):
    meta_path = test_path + ".meta"
    if not os.path.exists(test_path) or not os.path.exists(meta_path):
        return False
    with open(meta_path, "r", encoding="utf-8") as meta:
        stored_hash = meta.read()
    return stored_hash == hash_value

def group_operations_by_resource(paths):
    resource_groups = {}
    for path_key, methods in paths.items():
        # Extract resource name (e.g., 'posts' from '/posts/{id}')
        segments = [seg for seg in path_key.split('/') if seg and not seg.startswith('{')]
        if segments:
            resource = segments[0].lower()
        else:
            resource = "misc"
        if resource not in resource_groups:
            resource_groups[resource] = []
        for method, operation in methods.items():
            resource_groups[resource].append((path_key, method, operation))
    return resource_groups

if __name__ == "__main__":
    spec_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.json"))
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "generated-tests"))
    try:
        generate_pytest_tests_via_ai(spec_file, tests_dir)
        print("Pytest test generation completed successfully.")
    except Exception as err:
        print("Error:", err)
        exit(1)