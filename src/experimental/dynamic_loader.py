# src/experimental/dynamic_loader.py
import os
import sys
import importlib
import inspect
import logging
from typing import List
from src.core.base_engine import BaseCryptoEngine

def discover_experimental_engines() -> List[BaseCryptoEngine]:
    """
    Escanea dinámicamente la carpeta experimental/ en busca de clases que
    hereden de BaseCryptoEngine. Aísla fallas para no romper la ejecución global.
    """
    engines = []
    folder = os.path.dirname(__file__)
    
    if not os.path.exists(folder):
        return engines

    for file in os.listdir(folder):
        if file.endswith(".py") and file not in ["__init__.py", "dynamic_loader.py"]:
            # Construir la ruta absoluta del módulo para importlib
            module_name = f"src.experimental.{file[:-3]}"
            try:
                # Forzar la recarga o carga inicial limpia del plugin experimental
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])
                else:
                    module = importlib.import_module(module_name)
                
                # Buscar clases concretas que sigan el contrato del framework
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseCryptoEngine) and obj is not BaseCryptoEngine:
                        engines.append(obj())
            except Exception as e:
                # Registrar error crítico en el log persistente sin interrumpir el orquestador
                logging.error(f"[!] Error crítico al inyectar el plugin experimental {module_name}: {e}")
                continue
                
    return engines
