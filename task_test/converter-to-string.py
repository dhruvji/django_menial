import unittest
import os
import ast

class TestBackendsUtils(unittest.TestCase):

    def test_converter_to_string_class_exists(self):
        # Path to the file containing ConverterToString
        file_path = '../django/db/backends/utils.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Check if the ConverterToString class is defined
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        class_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'ConverterToString':
                class_found = True
                break

        self.assertTrue(class_found, "Class 'ConverterToString' not found in backends/utils.py")

    def test_converter_to_string_functions(self):
        # Path to the file containing ConverterToString
        file_path = '../django/db/backends/utils.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Check if the required functions are defined in ConverterToString class
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        functions = ['split_identifier', 'truncate_name', 'names_digest', 'format_number', 'strip_quotes']
        functions_found = {func: False for func in functions}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'ConverterToString':
                for class_node in ast.walk(node):
                    if isinstance(class_node, ast.FunctionDef) and class_node.name in functions_found:
                        functions_found[class_node.name] = True

        for func, found in functions_found.items():
            self.assertTrue(found, f"Function '{func}' not found in ConverterToString class")

    def test_converter_to_string_imports(self):
        files_to_test = [
            "../django/contrib/gis/db/backends/oracle/schema.py",
            "../django/db/backends/base/operations.py",
            "../django/db/backends/base/schema.py",
            "../django/db/backends/oracle/operations.py",
            "../django/db/backends/postgresql/creation.py",
            "../django/db/backends/postgresql/schema.py",
            "../django/db/backends/sqlite3/schema.py",
            #"../django/db/models/fields/related.py",
        ]

        for file_path in files_to_test:
            if not os.path.exists(file_path):
                print(f"File {file_path} not found.")
                continue

            with open(file_path, 'r') as file:
                tree = ast.parse(file.read())

            import_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module == 'django.db.backends.utils' and \
                       any(alias.name == 'ConverterToString' for alias in node.names):
                        import_found = True
                        break

            self.assertTrue(import_found, f"Import 'ConverterToString' not found in {file_path}")
            
    def check_function_call_in_file(self, file_path, function_name):
        """
        Helper function to check if a given function is called by a ConverterToString object in a specific file.
        """
        if not os.path.exists(file_path):
            self.fail(f"File {file_path} not found.")

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == function_name:
                    # Check if the object calling the function is an instance of ConverterToString
                    if self.is_converter_to_string(tree, node.func.value):
                        return True

        self.fail(f"Function '{function_name}' was not called by a ConverterToString object in {file_path}")

    def is_converter_to_string(self, tree, node):
        """
        Check if the given node is an instance of ConverterToString by tracing assignments in the AST.
        """
        if isinstance(node, ast.Name):
            for n in ast.walk(tree):
                if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == node.id:
                    if isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == 'ConverterToString':
                        return True
        return False

    # Test functions for split_identifier
    def test_split_identifier_called_in_test_utils_py(self):
        self.check_function_call_in_file("../tests/backends/test_utils.py", "split_identifier")

    def test_split_identifier_called_in_schema_py(self):
        self.check_function_call_in_file("../django/db/backends/base/schema.py", "split_identifier")

    def test_split_identifier_called_in_indexes_py(self):
        self.check_function_call_in_file("../django/db/models/indexes.py", "split_identifier")

    # Test functions for truncate_name
    def test_truncate_name_called_in_oracle_schema_py(self):
        self.check_function_call_in_file("../django/contrib/gis/db/backends/oracle/schema.py", "truncate_name")

    def test_truncate_name_called_in_models_options_py(self):
        self.check_function_call_in_file("../django/db/models/options.py", "truncate_name")

    def test_truncate_name_called_in_oracle_operations_py(self):
        self.check_function_call_in_file("../django/db/backends/oracle/operations.py", "truncate_name")

    def test_truncate_name_called_in_fields_related_py(self):
        self.check_function_call_in_file("../django/db/models/fields/related.py", "truncate_name")

    def test_truncate_name_called_in_base_schema_py(self):
        self.check_function_call_in_file("../django/db/backends/base/schema.py", "truncate_name")

    def test_truncate_name_called_in_test_utils_py(self):
        self.check_function_call_in_file("../tests/backends/test_utils.py", "truncate_name")

    def test_truncate_name_called_in_model_package_tests_py(self):
        self.check_function_call_in_file("../tests/model_package/tests.py", "truncate_name")

    def test_truncate_name_called_in_migrations_test_commands_py(self):
        self.check_function_call_in_file("../tests/migrations/test_commands.py", "truncate_name")

    def test_truncate_name_called_in_schema_tests_py(self):
        self.check_function_call_in_file("../tests/schema/tests.py", "truncate_name")

    # Test functions for names_digest
    def test_names_digest_called_in_base_schema_py(self):
        self.check_function_call_in_file("../django/db/backends/base/schema.py", "names_digest")

    def test_names_digest_called_in_indexes_py(self):
        self.check_function_call_in_file("../django/db/models/indexes.py", "names_digest")

    # Test functions for format_number
    def test_format_number_called_in_base_operations_py(self):
        self.check_function_call_in_file("../django/db/backends/base/operations.py", "format_number")

    def test_format_number_called_in_test_utils_py(self):
        self.check_function_call_in_file("../tests/backends/test_utils.py", "format_number")

    # Test functions for strip_quotes
    def test_strip_quotes_called_in_postgresql_creation_py(self):
        self.check_function_call_in_file("../django/db/backends/postgresql/creation.py", "strip_quotes")

    def test_strip_quotes_called_in_oracle_schema_py(self):
        self.check_function_call_in_file("../django/contrib/gis/db/backends/oracle/schema.py", "strip_quotes")

    def test_strip_quotes_called_in_oracle_operations_py(self):
        self.check_function_call_in_file("../django/db/backends/oracle/operations.py", "strip_quotes")

    def test_strip_quotes_called_in_fields_related_py(self):
        self.check_function_call_in_file("../django/db/models/fields/related.py", "strip_quotes")

    def test_strip_quotes_called_in_sqlite3_schema_py(self):
        self.check_function_call_in_file("../django/db/backends/sqlite3/schema.py", "strip_quotes")

    def test_strip_quotes_called_in_postgresql_schema_py(self):
        self.check_function_call_in_file("../django/db/backends/postgresql/schema.py", "strip_quotes")

if __name__ == '__main__':
    unittest.main()
