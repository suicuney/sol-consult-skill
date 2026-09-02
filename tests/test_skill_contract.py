#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_is_plan_review_only(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "name: sol-high-plan-review",
            "Codex = Plan Owner",
            "Sol High = Independent Plan Critic",
            "Maximum review rounds",
            "3",
            "PLAN FROZEN",
            "Do not call Sol High again",
        ):
            self.assertIn(required, skill)

    def test_mcp_is_single_browser_path(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        workflow = (SKILL_DIR / "references/mcp-workflow.md").read_text(encoding="utf-8")
        self.assertIn("Chrome DevTools MCP only", skill)
        self.assertIn("Model family = GPT-5.6 Sol", workflow)
        self.assertIn("Reasoning     = High", workflow)
        self.assertIn("Pro           # GPT-5.6 Sol Pro, not this workflow", workflow)
        self.assertIn("Do not silently fall back", workflow)

    def test_required_public_files_exist(self) -> None:
        for relative in (
            "agents/openai.yaml",
            "references/mcp-workflow.md",
            "references/context-packet-template.md",
            "scripts/check_packet_safety.py",
            "scripts/build_attachment_bundle.py",
        ):
            self.assertTrue((SKILL_DIR / relative).is_file(), relative)

    def test_evals_cover_core_boundaries(self) -> None:
        payload = json.loads((SKILL_DIR / "evals/evals.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in payload["evals"]}
        self.assertTrue({
            "plan-review-default",
            "skip-review-explicit",
            "max-three-rounds",
            "frozen-plan-exits-sol",
            "mcp-unavailable-no-fallback",
        }.issubset(ids))

    def test_no_personal_absolute_paths(self) -> None:
        for path in SKILL_DIR.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for forbidden in ("/Users/" + "me/", "zhu" + "jinpeng", "deepsight_" + "vault"):
                    self.assertNotIn(forbidden, text, str(path))


if __name__ == "__main__":
    unittest.main()
