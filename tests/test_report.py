import unittest

from iadp.diagnostics.report import DiagnosticReport


class TestDiagnosticReport(unittest.TestCase):
    def test_evidence_state_and_stable_digest(self):
        report = DiagnosticReport(generated_at="2026-10-07T00:00:00+00:00")
        report.add_evidence({
            "source": "simulator",
            "observed_at": "2026-10-07T00:00:00+00:00",
            "evidence_state": "observed",
            "raw": "410c1af8",
        })
        first = report.digest()
        self.assertEqual(first, report.digest())

    def test_rejects_untracked_state(self):
        report = DiagnosticReport(generated_at="2026-10-07T00:00:00+00:00")
        with self.assertRaises(ValueError):
            report.add_evidence({
                "source": "unknown",
                "observed_at": "2026-10-07T00:00:00+00:00",
                "evidence_state": "fact",
            })


if __name__ == "__main__":
    unittest.main()
