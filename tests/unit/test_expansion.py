from copy import deepcopy
from pathlib import Path
import shutil
import pytest
from chainmax.pipeline import load_config,construction_config
from chainmax.identity import DATASET_NAME,CATALOG_PATH


def test_2k_quota_configuration():
    c,h=load_config("configs/v1.yaml")
    assert DATASET_NAME==c["dataset_name"]=="chainmax-2k"
    assert CATALOG_PATH=="data/chainmax-2k.jsonl"
    assert c["target_base_instances"]==2000
    assert c["instances_per_family"]==200
    assert c["instances_per_family_level"]==50
    assert c["review"]["minimum_second_review_records"]==200


def test_explicit_migration_preserves_original_config(tmp_path):
    (tmp_path/"configs").mkdir()
    shutil.copyfile("configs/chainmax-1k.yaml",tmp_path/"configs/chainmax-1k.yaml")
    c,ch=load_config("configs/v1.yaml")
    old,old_hash=load_config("configs/chainmax-1k.yaml")
    rec={"instance_id":"cmx_000001","provenance":{"config_hash":old_hash,"dataset_migration":{"from_dataset":"ChainMax-1K","dataset_config_hash":ch}}}
    assert construction_config(tmp_path,rec,c,ch)==old
    same=deepcopy(rec); same["provenance"]={"config_hash":ch}
    assert construction_config(tmp_path,same,c,ch)==c
    for bad in ("missing_migration","wrong_target_config","new_id"):
        changed=deepcopy(rec)
        if bad=="missing_migration": del changed["provenance"]["dataset_migration"]
        if bad=="wrong_target_config": changed["provenance"]["dataset_migration"]["dataset_config_hash"]="wrong"
        if bad=="new_id": changed["instance_id"]="cmx_001001"
        with pytest.raises(ValueError): construction_config(tmp_path,changed,c,ch)
