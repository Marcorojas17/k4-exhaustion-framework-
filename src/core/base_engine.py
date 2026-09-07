# src/core/base_engine.py
from abc import ABC, abstractmethod
from typing import Iterator, Any

class BaseCryptoEngine(ABC):
    """
    Interfaz abstracta (ABC) obligatoria para todos los motores criptográficos.
    Garantiza la inyección de dependencias y la compatibilidad con el orquestador.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Devuelve el nombre único del algoritmo o familia criptográfica."""
        pass

    @abstractmethod
    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves de forma eficiente empleando Lazy Evaluation 
        (generadores iterables) para mitigar el consumo de memoria RAM.
        """
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Lógica pura de descifrado matemático. Devuelve la cadena de texto plano
        evaluable.
        """
        pass
