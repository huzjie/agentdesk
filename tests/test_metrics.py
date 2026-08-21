"""Metrics tests."""
import unittest

from agentdesk.observability import Metrics


class TestMetrics(unittest.TestCase):
    def test_counter(self):
        m = Metrics()
        m.inc("req_total", 2)
        m.inc("req_total", 3)
        self.assertEqual(m.get_counter("req_total"), 5)

    def test_prometheus(self):
        m = Metrics()
        m.inc("req_total")
        m.observe("latency", 0.5)
        out = m.render_prometheus()
        self.assertIn("req_total 1.0", out)
        self.assertIn("latency_avg", out)


if __name__ == "__main__":
    unittest.main()
