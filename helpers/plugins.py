from pathlib import Path
from importlib import import_module

def is_loadable_domain(directory):
    if directory.is_file():
        return False

    name = str(directory)
    return "__pycache__" not in name


def register_domains(parent):
    domains_folder = Path("./domain")
    domains = [
        str(domain).replace("/", ".")
        for domain in domains_folder.iterdir()
        if is_loadable_domain(domain)
    ]

    for domain in domains:
        try:
            register_error = import_module(f"{domain}")

            if "execute" in dir(register_error):
                register_error.execute()

            routes = import_module(f"{domain}.routes")
            routes.add_routes(parent)
        except ImportError as err:
            print(err)
