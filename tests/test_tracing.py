"""Tracing tests."""
import unittest

from agentdesk.observability import TraceContext


class TestTracing(unittest.TestCase):
    def test_child(self):
        t = TraceContext()
        c = t.child()
        self.assertEqual(c.trace_id, t.trace_id)
        self.assertEqual(c.parent_id, t.span_id)

    def test_traceparent_roundtrip(self):
        t = TraceContext()
        h = t.to_traceparent()
        t2 = TraceContext.from_traceparent(h)
        self.assertEqual(t2.trace_id, t.trace_id)
        self.assertEqual(t2.span_id, t.span_id)


if __name__ == "__main__":
    unittest.main()
