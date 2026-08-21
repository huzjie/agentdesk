"""Provider tests."""
import unittest

from agentdesk.providers import (
    MockProvider, OpenAIProvider, AnthropicProvider, DeepSeekProvider,
    QwenProvider, KimiProvider, GLMProvider, GeminiProvider, OllamaProvider,
)


class TestProviders(unittest.TestCase):
    def test_names(self):
        self.assertEqual(MockProvider().name, "mock")
        self.assertEqual(OpenAIProvider().name, "openai")
        self.assertEqual(AnthropicProvider().name, "anthropic")
        self.assertEqual(DeepSeekProvider().name, "deepseek")
        self.assertEqual(QwenProvider().name, "qwen")
        self.assertEqual(KimiProvider().name, "kimi")
        self.assertEqual(GLMProvider().name, "glm")
        self.assertEqual(GeminiProvider().name, "gemini")
        self.assertEqual(OllamaProvider().name, "ollama")

    def test_mock_chat(self):
        p = MockProvider()
        r = p.chat([{"role": "user", "content": "write a file"}])
        self.assertIn("tool_call", r["content"])


if __name__ == "__main__":
    unittest.main()
