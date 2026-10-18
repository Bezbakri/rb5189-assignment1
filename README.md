# Python Rekor Monitor Template

Assignment code for NYU CS-GY 9223 Software Supply Chain Security.

This program allows you to verify Rekor Transparency logs. You can check if a certain file matches a Rekor log index, get the latest checkpoint, or verify the consistency of a given checkpoint with the latest checkpoint.

## Installation:

Install all the project dependancies with ``poetry install``

## Usage:

```
usage: main.py [-h] [-d] [-c] [--inclusion INCLUSION] [--artifact ARTIFACT] [--consistency] [--tree-id TREE_ID]
               [--tree-size TREE_SIZE] [--root-hash ROOT_HASH]

Rekor Verifier

options:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode
  -c, --checkpoint      Obtain latest checkpoint from Rekor Server public instance
  --inclusion INCLUSION
                        Verify inclusion of an entry in the Rekor Transparency Log using log index and artifact
                        filename. Usage: --inclusion 126574567
  --artifact ARTIFACT   Artifact filepath for verifying signature
  --consistency         Verify consistency of a given checkpoint with the latest checkpoint.
  --tree-id TREE_ID     Tree ID for consistency proof
  --tree-size TREE_SIZE
                        Tree size for consistency proof
  --root-hash ROOT_HASH
                        Root hash for consistency proof
```

## Development Instructions

In order to add features to this project, please create a fork and use a pull request in order to push changes to the project.