"""Skill registration and search demo."""
from agentdesk.skills import SkillRegistry, SkillDef


def main():
    reg = SkillRegistry()
    reg.register(SkillDef(name="text_summary", version="1.0.0",
                          description="summarize text", tags=["nlp"]))
    reg.register(SkillDef(name="text_summary", version="1.1.0",
                          description="summarize text v2", tags=["nlp"]))

    latest = reg.get_by_name("text_summary")
    print("latest version:", latest.version)

    for s in reg.list(query="summar"):
        print("search hit:", s.name, s.version)


if __name__ == "__main__":
    main()
