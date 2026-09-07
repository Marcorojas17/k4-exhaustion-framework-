from typing import Iterator, Any, Dict, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class VicFractionalEngine(BaseCryptoEngine):
    @property
    def name(self) -> str:
        return "VicFractionalCipher"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        parser = ImageKeyParser()
        try:
            m3_data = parser.extract_matrix_mod26("matrix_3.png", size=25)
        except:
            m3_data = None
        common_rows = [(2,6),(1,5),(3,7),(4,8)]
        for row_indices in common_rows:
            for shift in range(10):
                yield (row_indices, shift)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        row_indices, shift = key
        blank1, blank2 = row_indices
        alphabet = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
        board: Dict[str, str] = {}
        digits = [(i + shift) % 10 for i in range(10)]
        alpha_idx = 0
        for d in digits:
            if d == blank1 or d == blank2:
                continue
            if alpha_idx < len(alphabet):
                board[str(d)] = alphabet[alpha_idx]
                alpha_idx += 1
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank1}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1
        for d in digits:
            if alpha_idx < len(alphabet):
                board[f"{blank2}{d}"] = alphabet[alpha_idx]
                alpha_idx += 1

        length = len(ciphertext)
        columns = 10
        rows = (length // columns) + (1 if length % columns!= 0 else 0)
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
                if grid[r][c]!= '':
                    flattened.append(grid[r][c])
        transposed_text = "".join(flattened)

        final_chars: List[str] = []
        i = 0
        while i < len(transposed_text):
            char = transposed_text[i]
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
