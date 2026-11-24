import unittest
from evaluate import summarize, load_rows
from pathlib import Path


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_rows(Path(__file__).with_name('sample.json'))

    def test_aggregation(self):
        a, b = summarize(self.rows)
        self.assertEqual(a['overall_percent'], 91.67)
        self.assertEqual(b['overall_percent'], 16.67)
        self.assertEqual(len(b['failures']), 2)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            summarize(self.rows + [self.rows[0]])

    def test_invalid_score(self):
        self.rows[0]['accuracy'] = 3
        with self.assertRaises(ValueError):
            summarize(self.rows)

    def test_boolean_score(self):
        self.rows[0]['accuracy'] = True
        with self.assertRaises(ValueError):
            summarize(self.rows)

    def test_csv_score_strings(self):
        self.rows[0]['accuracy'] = '2'
        self.assertEqual(summarize(self.rows)[0]['accuracy'], 2)


if __name__ == '__main__':
    unittest.main()
