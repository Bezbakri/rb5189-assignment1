import subprocess

import main


def test_bad_signature():
    bad_log_index = "3042934852"
    art_file = "artifact.md"
    result = subprocess.run(
        ["python", "main.py", "--inclusion", bad_log_index, "--artifact", art_file],
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert output == "Given log index does not have a signature\n"
