from main import get_verification_proof

def test_invalid_log_index():
    log_index = "30000000000"

    result = get_verification_proof(log_index)

    assert result == "No log index found"