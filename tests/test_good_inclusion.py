import subprocess

import main


def test_good_inclusion():
    log_index = "3042934851"
    art_file = "artifact.md"
    result = subprocess.run(
        ["python", "main.py", "--inclusion", log_index, "--artifact", art_file],
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert output == "Offline verification successful\n"
