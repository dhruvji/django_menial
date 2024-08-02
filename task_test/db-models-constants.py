import unittest
import os
import ast

class TestORMConstantsMigration(unittest.TestCase):

    def test_constants_moved_to_base(self):
        # Path to the old constants.py file
        old_file_path = '/data/dhruv_gautam/django_menial/django/db/models/constants.py'
        # Path to the new base.py file
        new_file_path = '/data/dhruv_gautam/django_menial/django/db/models/base.py'

        # Ensure old constants file does not contain the constants
        if os.path.exists(old_file_path):
            with open(old_file_path, 'r') as file:
                old_tree = ast.parse(file.read())
            
            old_constants = [node for node in ast.walk(old_tree) if isinstance(node, ast.Assign)]
            old_enums = [node for node in ast.walk(old_tree) if isinstance(node, ast.ClassDef) and node.name == 'OnConflict']

            self.assertFalse(any(node.targets[0].id == 'LOOKUP_SEP' for node in old_constants),
                             "'LOOKUP_SEP' should not be in constants.py")
            self.assertFalse(any(node.name == 'OnConflict' for node in old_enums),
                             "'OnConflict' enum should not be in constants.py")
        
        # Ensure new base.py file contains the constants
        self.assertTrue(os.path.exists(new_file_path), f"{new_file_path} does not exist")

        with open(new_file_path, 'r') as file:
            new_tree = ast.parse(file.read())

        new_constants = [node for node in ast.walk(new_tree) if isinstance(node, ast.Assign)]
        new_enums = [node for node in ast.walk(new_tree) if isinstance(node, ast.ClassDef) and node.name == 'OnConflict']

        self.assertTrue(any(node.targets[0].id == 'LOOKUP_SEP' for node in new_constants),
                        "'LOOKUP_SEP' not found in base.py")
        self.assertTrue(any(node.name == 'OnConflict' for node in new_enums),
                        "'OnConflict' enum not found in base.py")

    def test_imports_updated_to_base(self):
        # List of files that should have updated imports
        files_to_check = [
            '../django/contrib/admin/checks.py',
            '../django/contrib/admin/options.py',
            '../django/contrib/admin/templatetags/admin_list.py',
            '../django/contrib/admin/utils.py',
            '../django/contrib/admin/views/main.py',
            '../django/core/management/commands/inspectdb.py',
            '../django/db/backends/mysql/operations.py',
            '../django/db/backends/mysql/schema.py',
            '../django/db/backends/postgresql/operations.py',
            '../django/db/backends/sqlite3/operations.py',
            '../django/db/models/constraints.py',
            '../django/db/models/expressions.py',
            '../django/db/models/fields/__init__.py',
            '../django/db/models/fields/json.py',
            '../django/db/models/fields/related.py',
            '../django/db/models/query.py',
            '../django/db/models/query_utils.py',
            '../django/db/models/sql/compiler.py',
            '../django/db/models/sql/query.py',
        ]

        for file_path in files_to_check:
            self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

            with open(file_path, 'r') as file:
                tree = ast.parse(file.read())

            imports_updated = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module == 'django.db.models.base' and \
                       any(alias.name == 'LOOKUP_SEP' or alias.name == 'OnConflict' for alias in node.names):
                        imports_updated = True
                        break

            self.assertTrue(imports_updated, f"Imports of 'LOOKUP_SEP' or 'OnConflict' not updated to 'base' in {file_path}")

    def test_on_conflict_reference_exists(self):
        # Path to the documentation file
        docs_file_path = '../docs/releases/4.1.txt'

        # Check if the documentation file exists
        self.assertTrue(os.path.exists(docs_file_path), f"Documentation file {docs_file_path} does not exist")

        # Open and read the contents of the documentation file
        with open(docs_file_path, 'r') as file:
            docs_content = file.read()

        # Reference to check
        reference = "django.db.models.base.OnConflict"

        # Check that the reference exists
        self.assertIn(reference, docs_content, f"Reference '{reference}' not found in release notes")

if __name__ == '__main__':
    unittest.main()
