from src.integrations.telegram.command_parser import parse_command


def test_brainstorm_inline_command_name():
    cmd = parse_command("/brainstormWithProductManager 用户增长要点")
    assert cmd is not None
    assert cmd.name == "brainstormWithProductManager"
    assert cmd.args == ["用户增长要点"]


def test_generate_codex_prompt_with_flags():
    cmd = parse_command("/generateCodexPrompt myProject --module auth")
    assert cmd is not None
    assert cmd.name == "generateCodexPrompt"
    assert cmd.args == ["myProject", "--module", "auth"]
