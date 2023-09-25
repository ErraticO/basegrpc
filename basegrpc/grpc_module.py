import importlib
import glob


class MLModule:
    def __init__(self):
        self.module_name = ""
        self.module_path = ""

    def load_module(self):
        module_path = self.find_module_path()
        self.module_path = module_path
        if module_path:
            module = importlib.import_module(module_path)
            parts = module_path.rsplit(".", 1)
            if len(parts) == 1:
                model_service = getattr(module, parts[0])
            else:
                model_service = getattr(module, parts[1])
            return model_service()

    def find_module_path(self):
        module_paths = [file.replace("\\", ".").replace("/", ".").replace(".py", "") for file in
                        glob.glob('**/*.py', recursive=True)]
        if self.module_name == "":
            matches = ['grpc', 'test', '__init__', 'setup']
            for module_path in module_paths:
                if not any(x in module_path for x in matches):
                    return module_path
        else:
            for module_path in module_paths:
                if self.module_name in module_path:
                    return module_path


ml_module = MLModule()
