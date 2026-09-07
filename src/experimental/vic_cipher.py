# src/experimental/vic_cipher.py
from typing import Iterator, Any, List, Dict
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class VicFractionalEngine(BaseCryptoEngine):
    """
    Implementación adaptada del Cifrado VIC Soviético de la Guerra Fría para el K4.
    Utiliza un tablero de ajedrez expandido (Straddling Checkerboard) y transposición irregular.
    """

    @property
    def name(self) -> str:
        return "VicFractionalCipher"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera configuraciones de tablero combinadas con permutaciones de transposición.
        Extrae datos geométricos de la matrix_3 y matrix_4 como base.
        """
        parser = ImageKeyParser()
        m3_data = parser.extract_matrix_mod26("matrix_3.png", size=25)
        
        # Combinaciones de filas en blanco estándar usadas por espías
        common_rows = [
            (2, 6), (1, 5), (3, 7), (4, 8)
        ]
        
        # Barremos desfases de alineación (0-9) sobre las filas de la cuadrícula
        for row_indices in common_rows:
            for shift in range(10):
                yield (row_indices, shift)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Deshace primero la transposición columnar asimétrica y luego decodifica
        los valores fraccionarios a través del Straddling Checkerboard.
        """
        row_indices, shift = key
        blank1, blank2 = row_indices

        # 1. Reconstrucción del Straddling Checkerboard polialfabético
        alphabet = "KRYPTOSABCDEFGHIJLMNQUVWXZ" 
        board: Dict[str, str] = {}
        
        # Generar permutación de dígitos mod 10 basados en el desplazamiento
        digits = [(i + shift) % 10 for i in range(10)]
        
        alpha_idx = 0
        # Fila 1: Caracteres directos en posiciones sin huecos
        for d in digits:
            if d == blank1 or d == blank2:
                continue
            if alpha_idx < len(alphabet):
                board[str(d)] = alphabet[alpha_idx]
                alpha_idx += 1

        # Fila 2: Coordenadas compuestas (blank1 + d)
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank1}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1

        # Fila 3: Coordenadas compuestas (blank2 + d)
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank2}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1

        # 2. Deshacer Transposición Columnar Irregular de 10 columnas
        length = len(ciphertext)
        columns = 10
        rows = (length // columns) + (1 if length % columns != 0 else 0)
        
        col_order = sorted(range(len(digits)), key=lambda k: digits[k])
        col_lengths = [rows - 1] * columns
        remainder = length % columns
        
        for i in range(remainder if remainder > 0 else columns):
            col_lengths[col_order[i]] += 1

        grid = [['' for _ in range(columns)] for _ in range(rows)]
        idx = 0
        
        for c in col_order:
            for r in range(col_lengths[c]):
                if idx < length:
                    grid[r][c] = ciphertext[idx]
                    idx += 1

        flattened = []
        for r in range(rows):
            for c in range(columns):
               # src/experimental/vic_cipher.py
from typing import Iterator, Any, List, Dict
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class VicFractionalEngine(BaseCryptoEngine):
    """
    Implementación adaptada del Cifrado VIC Soviético de la Guerra Fría para el K4.
    Utiliza un tablero de ajedrez expandido (Straddling Checkerboard) y transposición irregular.
    """

    @property
    def name(self) -> str:
        return "VicFractionalCipher"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera configuraciones de tablero combinadas con permutaciones de transposición.
        Extrae datos geométricos de la matrix_3 y matrix_4 como base.
        """
        parser = ImageKeyParser()
        m3_data = parser.extract_matrix_mod26("matrix_3.png", size=25)
        
        # Combinaciones de filas en blanco estándar usadas por espías
        common_rows = [
            (2, 6), (1, 5), (3, 7), (4, 8)
        ]
        
        # Barremos desfases de alineación (0-9) sobre las filas de la cuadrícula
        for row_indices in common_rows:
            for shift in range(10):
                yield (row_indices, shift)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Deshace primero la transposición columnar asimétrica y luego decodifica
        los valores fraccionarios a través del Straddling Checkerboard.
        """
        row_indices, shift = key
        blank1, blank2 = row_indices

        # 1. Reconstrucción del Straddling Checkerboard polialfabético
        alphabet = "KRYPTOSABCDEFGHIJLMNQUVWXZ" 
        board: Dict[str, str] = {}
        
        # Generar permutación de dígitos mod 10 basados en el desplazamiento
        digits = [(i + shift) % 10 for i in range(10)]
        
        alpha_idx = 0
        # Fila 1: Caracteres directos en posiciones sin huecos
        for d in digits:
            if d == blank1 or d == blank2:
                continue
            if alpha_idx < len(alphabet):
                board[str(d)] = alphabet[alpha_idx]
                alpha_idx += 1

        # Fila 2: Coordenadas compuestas (blank1 + d)
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank1}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1

        # Fila 3: Coordenadas compuestas (blank2 + d)
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank2}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1

        # 2. Deshacer Transposición Columnar Irregular de 10 columnas
        length = len(ciphertext)
        columns = 10
        rows = (length // columns) + (1 if length % columns != 0 else 0)
        
        col_order = sorted(range(len(digits)), key=lambda k: digits[k])
        col_lengths = [rows - 1] * columns
        remainder = length % columns
        
        for i in range(remainder if remainder > 0 else columns):
            col_lengths[col_order[i]] += 1

        grid = [['' for _ in range(columns)] for _ in range(rows)]
        idx = 0
        
        for c in col_order:
            for r in range(col_lengths[c]):
                if idx < length:
                    grid[r][c] = ciphertext[idx]
                    idx += 1

        flattened = []
        for r in range(rows):
            for c in range(columns):
                if grid[r][c] != '':
                    flattened.append(grid[r][c])
        
        transposed_text = "".join(flattened)

        # 3. Decodificación fraccionaria inversa
        final_chars: List[str] = []
        i = 0
        while i < len(transposed_text):
            char = transposed_text[i]
            # Mapear letras del criptograma intermedio a dígitos simulados mod 10
            val_str = str((ord(char) - 65) % 10)
            
            if val_str == str(blank1) or val_str == str(blank2):
                if i + 1 < len(transposed_text):
                    next_val = str((ord(transposed_text[i+1]) - 65) % 10)
                    lookup = val_str + next_val
                    final_chars.append(board.get(lookup, "?"))
                    i += 2
                else:
                    final_chars.append("?")
                    i += 1
            else:
                final_chars.append(board.get(val_str, "?"))
                i += 1

        return "".join(final_chars)
 if grid[r][c] != '':
                    flattened.append(grid[r][c])
        
        transposed_text = "".join(flattened)

        # 3. Decodificación fraccionaria inversa
        final_chars: List[str] = []
        i = 0
        while i < len(transposed_text):
            char = transposed_text[i]
            # Mapear letras del criptograma intermedio a dígitos simulados mod 10
            val_str = str((ord(char) - 65) % 10)
            
            if val_str == str(blank1) or val_str == str(blank2):
                if i + 1 < len(transposed_text):
                    next_val = str((ord(transposed_text[i+1]) - 65) % 10)
                    lookup = val_str + next_val
                    final_chars.append(board.get(lookup, "?"))
                    i += 2
                else:
                    final_chars.append("?")
                    i += 1
            else:
                final_chars.append(board.get(val_str, "?"))
                i += 1

        return "".join(final_chars)
