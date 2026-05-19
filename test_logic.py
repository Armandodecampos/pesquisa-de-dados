import unittest
import os
import pandas as pd
from process_data import normalize_text, process_excel, filter_items

class TestDataProcessing(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("Olá Mundo"), "ola mundo")
        self.assertEqual(normalize_text("Ação e Reação"), "acao e reacao")
        self.assertEqual(normalize_text("   TESTE   "), "teste")

    def test_filter_items(self):
        items = [
            {"search_text": "joao silva 123 ti", "department": "TI", "nome": "Joao"},
            {"search_text": "maria oliveira 456 rh", "department": "RH", "nome": "Maria"}
        ]
        self.assertEqual(len(filter_items(items, "joao")), 1)
        self.assertEqual(len(filter_items(items, "rh")), 1)
        self.assertEqual(len(filter_items(items, "xyz")), 0)
        self.assertEqual(len(filter_items(items, "joao", ["RH"])), 0)

    def test_process_excel(self):
        # Create a mock excel file
        file_path = "test_mock.xlsx"
        data = [
            [123, "Joao", "Silva", None, "TI", None, None, "1199999", "joao@email.com", "joao@work.com"],
            [456, "Maria", "Oliveira", None, "RH", None, None, "1188888", "maria@card.com", "maria@email.com"]
        ]
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, header=False)

        try:
            processed = process_excel(file_path)
            self.assertEqual(len(processed), 2)
            self.assertEqual(processed[0]["nome"], "Joao")
            self.assertEqual(processed[1]["department"], "RH")
            self.assertIn("joao", processed[0]["search_text"])
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    unittest.main()
