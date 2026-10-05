from safety.validator import SafetyValidator


def test_destructive_action_is_blocked():
    validator = SafetyValidator()

    result = validator.validate(
        "delete_all",
        {},
    )

    assert result.allowed is False


def test_valid_move_is_allowed():
    validator = SafetyValidator()

    result = validator.validate(
        "move_file",
        {
            "source": "report.pdf",
            "destination": "documents/report.pdf",
        },
    )

    assert result.allowed is True
