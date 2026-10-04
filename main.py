import argparse
from util import extract_public_key, verify_artifact_signature
from merkle_proof import DefaultHasher, verify_consistency, verify_inclusion, compute_leaf_hash
import requests
import json
import os
import base64

def get_log_entry(log_index, debug=False):
    # TODO: verify that log index value is sane
    # Get the request data
    check_log_index = requests.get("https://rekor.sigstore.dev/api/v1/log/entries", params={"logIndex": log_index})
    if check_log_index.status_code == 200:
        log_json_data = check_log_index.json()
        log_uuid = list(log_json_data.keys())[0]
        if debug == True:
            print("Got a 200")
            # print(log_uuid)
            # print(log_json_data[log_uuid]['body'])
        return log_uuid, log_json_data[log_uuid]
    else:
        # didn't get what i wanted
        return "No log index found"

def get_verification_proof(log_index, debug=False):
    # TODO: verify that log index value is sane
    log_entry = get_log_entry(log_index, debug)
    if log_entry == "No log index found":
        return log_entry
    log_uuid, log_json_data = log_entry
    verification_data = log_json_data['verification']
    index = verification_data['inclusionProof']['logIndex']
    hashes = verification_data['inclusionProof']['hashes']
    root_hash = verification_data['inclusionProof']['rootHash']
    tree_size = verification_data['inclusionProof']['treeSize']
    return index, tree_size, hashes, root_hash

def inclusion(log_index, artifact_filepath, debug=False):
    # TODO::
    # verify that log index and artifact filepath values are sane
    log_entry = get_log_entry(log_index, debug)
    if log_entry == "No log index found":
        print(log_entry)
        return
    log_uuid, log_json_data = log_entry
    if not os.path.exists(artifact_filepath):
        print("Invalid file path")
        return
    log_body_b64 = log_json_data['body']
    log_body = base64.b64decode(log_body_b64)
    log_body_json = json.loads(log_body.decode())
    # if debug:
    #     print(log_body)
    #     print(log_body_json)
    signature_b64 = log_body_json['spec']['signature']['content']
    signature = base64.b64decode(signature_b64)
    public_key_b64 = log_body_json['spec']['signature']['publicKey']['content']
    certificate = base64.b64decode(public_key_b64)
    public_key = extract_public_key(certificate)
    if debug:
        print(public_key.decode())
    verify_artifact_signature(signature, public_key, artifact_filepath)
    index, tree_size, hashes, root_hash = get_verification_proof(log_index)
    leaf_hash = compute_leaf_hash(log_body_b64)
    verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)
    print("Offline verification successful")    

def get_latest_checkpoint(debug=False):
    # TODO: Fetch the latest checkpoint from rekor
    latest_checkpoint = requests.get("https://rekor.sigstore.dev/api/v1/log")
    if latest_checkpoint.status_code == 200:
        latest_checkpoint_json = latest_checkpoint.json()
        if debug:
            print("Got a 200")
        return latest_checkpoint_json
    else:
        return "Fatal error: no checkpoint found"

def consistency(prev_checkpoint, debug=False):
    # TODO: 
    # verify that prev checkpoint is not empty
    if "treeID" not in prev_checkpoint or "treeSize" not in prev_checkpoint or "rootHash" not in prev_checkpoint:
        print("Empty prev checkpoint!")
        return
    latest_checkpoint = get_latest_checkpoint()
    latest_root_hash = latest_checkpoint["rootHash"]
    latest_tree_size = latest_checkpoint["treeSize"]
    # latest_tree_id = latest_checkpoint["treeID"] 
    prev_root_hash = prev_checkpoint["rootHash"]
    prev_tree_size = prev_checkpoint["treeSize"]
    # prev_tree_id = prev_checkpoint["treeID"]
    if prev_tree_size > latest_tree_size:
        print("Previous size cannot be bigger than latest size")
        return
    if prev_tree_size == latest_tree_size:
        proof = None
    else:
        proof_req = requests.get("https://rekor.sigstore.dev/api/v1/log/proof", params={"firstSize": prev_tree_size, "lastSize": latest_tree_size})
        if proof_req.status_code == 200:
            proof_req_json = proof_req.json()
            if debug:
                print("Got a 200")
            proof = proof_req_json["hashes"]
        else:
            return "Fatal error: no proof found"
    verify_consistency(DefaultHasher, prev_tree_size, latest_tree_size, proof, prev_root_hash, latest_root_hash)
    print("Consistency verification successful")
    

def main():
    debug = False
    parser = argparse.ArgumentParser(description="Rekor Verifier")
    parser.add_argument('-d', '--debug', help='Debug mode',
                        required=False, action='store_true') # Default false
    parser.add_argument('-c', '--checkpoint', help='Obtain latest checkpoint\
                        from Rekor Server public instance',
                        required=False, action='store_true')
    parser.add_argument('--inclusion', help='Verify inclusion of an\
                        entry in the Rekor Transparency Log using log index\
                        and artifact filename.\
                        Usage: --inclusion 126574567',
                        required=False, type=int)
    parser.add_argument('--artifact', help='Artifact filepath for verifying\
                        signature',
                        required=False)
    parser.add_argument('--consistency', help='Verify consistency of a given\
                        checkpoint with the latest checkpoint.',
                        action='store_true')
    parser.add_argument('--tree-id', help='Tree ID for consistency proof',
                        required=False)
    parser.add_argument('--tree-size', help='Tree size for consistency proof',
                        required=False, type=int)
    parser.add_argument('--root-hash', help='Root hash for consistency proof',
                        required=False)
    # # For testing
    # parser.add_argument('--log-index', help='Log index for get details of log entry',
    #                         required=False)
    args = parser.parse_args()
    if args.debug:
        debug = True
        print("enabled debug mode")
    # # For testing
    # if args.log_index:
    #     print(get_log_entry(args.log_index, debug))
    if args.checkpoint:
        # get and print latest checkpoint from server
        # if debug is enabled, store it in a file checkpoint.json
        checkpoint = get_latest_checkpoint(debug)
        print(json.dumps(checkpoint, indent=4))
    if args.inclusion:
        inclusion(args.inclusion, args.artifact, debug)
    if args.consistency:
        if not args.tree_id:
            print("please specify tree id for prev checkpoint")
            return
        if not args.tree_size:
            print("please specify tree size for prev checkpoint")
            return
        if not args.root_hash:
            print("please specify root hash for prev checkpoint")
            return

        prev_checkpoint = {}
        prev_checkpoint["treeID"] = args.tree_id
        prev_checkpoint["treeSize"] = args.tree_size
        prev_checkpoint["rootHash"] = args.root_hash

        consistency(prev_checkpoint, debug)

if __name__ == "__main__":
    main()
