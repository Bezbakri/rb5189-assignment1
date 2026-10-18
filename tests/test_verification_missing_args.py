import subprocess

import main


def test_verification_missing_args():
    tree_id = "1193050959916656506"
    tree_size = "5114308"
    root_hash = "aa9f28964e1205576a05cbc6b66222124142b9fb15d803f55d8cbb1d74e766d7"
    result1 = subprocess.run(
        [
            "python",
            "main.py",
            "--consistency",
            "--tree-size",
            tree_size,
            "--root-hash",
            root_hash,
        ],
        capture_output=True,
        text=True,
    )
    output1 = result1.stdout

    result2 = subprocess.run(
            [
                "python",
                "main.py",
                "--consistency",
                "--tree-id",
                tree_id,
                "--root-hash",
                root_hash,
            ],
            capture_output=True,
            text=True,
        )
    output2 = result2.stdout

    result3 = subprocess.run(
            [
                "python",
                "main.py",
                "--consistency",
                "--tree-id",
                tree_id,
                "--tree-size",
                tree_size,
            ],
            capture_output=True,
            text=True,
        )
    output3 = result3.stdout

    assert output1 == "please specify tree id for prev checkpoint\n"
    assert output2 == "please specify tree size for prev checkpoint\n"
    assert output3 == "please specify root hash for prev checkpoint\n"
