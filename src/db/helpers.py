import ast
import importlib.util


MODEL_BASE_CLASS_NAME = 'Model'
DYNAMIC_MODULE_NAME = 'dynamic_module'


class SubclassFinder(ast.NodeVisitor):
    def __init__(self, base_class_name):
        self.base_class_name = base_class_name
        self.subclasses = []

    def visit_ClassDef(self, node):
        if self._is_subclass_of_model(node):
            self.subclasses.append(node.name)
        self.generic_visit(node)

    def _is_subclass_of_model(self, node):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self.base_class_name:
                return True
        return False


def execute_get_init_sql_on_subclasses(file_path):
    subclasses = find_model_subclasses(file_path, MODEL_BASE_CLASS_NAME)
    module = import_file_as_module(file_path, DYNAMIC_MODULE_NAME)

    results = {}
    for subclass_name in subclasses:
        sql = _get_init_sql_from_class(module, subclass_name)
        results[subclass_name] = sql
    return results


def find_model_subclasses(file_path, base_class_name):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)
    finder = SubclassFinder(base_class_name)
    finder.visit(tree)
    return finder.subclasses


def import_file_as_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_init_sql_from_class(module, class_name):
    klass = getattr(module, class_name, None)
    if klass and hasattr(klass, 'get_init_sql') and callable(getattr(klass, 'get_init_sql')):
        instance = klass()
        return instance.get_init_sql()
    return None
