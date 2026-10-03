import unittest

from scripts.generate_script import build_script
from scripts.generate_topic import generate_topic


class ContentGenerationTests(unittest.TestCase):
    def test_generate_topic_is_deterministic_for_date(self) -> None:
        self.assertEqual(generate_topic("2026-09-16"), generate_topic("2026-09-16"))

    def test_generate_script_contains_topic_title(self) -> None:
        topic = "Detective Duck and the Missing Cupcakes"
        script = build_script(topic)
        self.assertIn(f"Title: {topic}", script)
        self.assertIn("Scene 1:", script)


if __name__ == "__main__":
    unittest.main()
