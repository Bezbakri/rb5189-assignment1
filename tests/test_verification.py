import subprocess

import main


def test_verification():
    tree_id = "1193050959916656506"
    tree_size = "5114308"
    root_hash = "aa9f28964e1205576a05cbc6b66222124142b9fb15d803f55d8cbb1d74e766d7"
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--consistency",
            "--tree-id",
            tree_id,
            "--tree-size",
            tree_size,
            "--root-hash",
            root_hash,
        ],
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert output == "Consistency verification successful\n"
