import importlib, pathlib, pkgutil
def discover_experimental_engines():
    engines=[]
    pkg_path=pathlib.Path(__file__).parent
    for _, mod_name, _ in pkgutil.iter_modules([str(pkg_path)]):
        if mod_name.startswith("vic"):
            try:
                mod=importlib.import_module(f"src.experimental.{mod_name}")
                for attr in dir(mod):
                    obj=getattr(mod, attr)
                    if hasattr(obj, 'name') and hasattr(obj, 'decrypt'):
                        try:
                            engines.append(obj())
                        except:
                            pass
            except Exception as e:
                print(f"[!] skip {mod_name}: {e}")
    return engines
