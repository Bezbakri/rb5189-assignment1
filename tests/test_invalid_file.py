import subprocess

import main


def test_invalid_file():
    log_index = "3042934851"
    art_file = "file_does_not_exist.txt"
    result = subprocess.run(
        ["python", "main.py", "--inclusion", log_index, "--artifact", art_file],
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert output == "Invalid file path\n"
