from src.core.idea_parser import IdeaParser


def test_parse_short_message():
    idea = IdeaParser.parse_input("Build an AI startup OS for idea-to-code")
    assert idea["title"]
    assert "summary" in idea


def test_parse_markdown_sections():
    md = """# Smart CRM\n\nNeed AI assistant CRM.\n\n## Requirements\n- Lead scoring\n- Pipeline tracking\n\n## Open Questions\n- Pricing model\n"""
    idea = IdeaParser.parse_markdown(md)
    assert idea["title"] == "Smart CRM"
    assert "Lead scoring" in idea["requirements"]
    assert "Pricing model" in idea["unknowns"]
