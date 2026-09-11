"""Tests for the evidence-review layer; these do not retrain the surrogate."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("project1_review", ROOT / "scripts/review_project1.py")
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class Project1EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = review.review_project(ROOT)

    def test_complete_grid_and_split(self):
        self.assertEqual(self.report["grid_rows"], 45)
        self.assertEqual(self.report["split_counts"], {"train_cv": 36, "test_holdout": 9})

    def test_final_result_tradeoff(self):
        self.assertAlmostEqual(self.report["knee_hydraulic_power_reduction_percent"], 63.53378222871247, places=8)
        self.assertAlmostEqual(self.report["knee_temperature_penalty_C"], 4.1069606687350415, places=8)

    def test_five_case_temperature_agreement(self):
        self.assertEqual(self.report["comparison_cases"], 5)
        self.assertLess(self.report["validation_metrics_recalculated"]["Maximum chip temperature"]["Max_absolute_error"], 0.10)

    def test_missing_energy_evidence_is_not_a_pass(self):
        self.assertEqual(self.report["missing_energy_balance_grid_rows"], 45)

    def test_metrics_perfect_prediction(self):
        result = review.error_metrics([1., 2., 3.], [1., 2., 3.])
        self.assertEqual(result["MAE"], 0.)
        self.assertEqual(result["R2"], 1.)

    def test_metrics_reject_mismatched_lists(self):
        with self.assertRaises(ValueError):
            review.error_metrics([1.], [1., 2.])

    def test_metrics_reject_zero_percentage_reference(self):
        with self.assertRaises(ValueError):
            review.error_metrics([0., 1.], [0., 1.])

    def test_metrics_reject_nonfinite_values(self):
        with self.assertRaises(ValueError):
            review.error_metrics([1.], [float("nan")])


if __name__ == "__main__":
    unittest.main()
