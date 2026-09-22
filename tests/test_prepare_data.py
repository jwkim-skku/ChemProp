import unittest

import pandas as pd

from src.prepare_data import TARGET_COLUMN, prepare_dataframe


class PrepareDataTest(unittest.TestCase):
    def test_derives_gap_and_filters_rows(self):
        frame = pd.DataFrame(
            {
                "uid": ["m1", "m2", "bad", "dup"],
                "smiles": ["CC", "CCC", "CO", "CC"],
                "S1_energy": [2.4, 3.1, 1.9, 2.4],
                "T1_energy": [2.0, 2.8, 1.2, 2.0],
            }
        )
        cleaned, summary = prepare_dataframe([frame], invalid_uids={"bad"})

        self.assertEqual(cleaned["uid"].tolist(), ["m1", "m2"])
        for actual, expected in zip(cleaned[TARGET_COLUMN], [0.4, 0.3]):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(
            summary,
            {
                "input_rows": 4,
                "removed_missing_or_invalid": 0,
                "removed_known_invalid_uids": 1,
                "removed_duplicate_smiles": 1,
                "output_rows": 2,
            },
        )

    def test_rejects_missing_schema(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            prepare_dataframe([pd.DataFrame({"smiles": ["CC"]})])


if __name__ == "__main__":
    unittest.main()
