import json
import os
from pathlib import Path
from modules.runtime.cli_adapter import validate_spec, dry_run, replay

def test_python_cli_adapter_golden_path(tmp_path: Path) -> None:
    # 1. Prepare paths
    spec_file = tmp_path / "spec.json"
    evidence_file = tmp_path / "evidence.jsonl"
    replay_file = tmp_path / "replay.json"
    
    # 2. Write valid AgentSpec
    spec_data = {
        "contract_name": "agent-spec",
        "schema_version": "v1",
        "agent_spec_id": "python-adapter-test",
        "intent": "validate",
        "goal": "Verify Python subprocess CLI adapter integration",
        "pipeline": ["echo-step"],
        "outputs": [{"kind": "json", "path": "evidence/run.json"}]
    }
    spec_file.write_text(json.dumps(spec_data))
    
    # 3. Test validate_spec
    res_val = validate_spec(str(spec_file))
    assert res_val.get("ok") is True
    assert res_val.get("contract_name") == "agent-spec"
    assert res_val.get("validated") is True
    
    # 4. Test dry_run
    res_run = dry_run(str(spec_file), str(evidence_file), str(replay_file))
    assert res_run.get("ok") is True
    assert res_run.get("status") == "success"
    assert "evidence_root_hash" in res_run
    
    assert evidence_file.exists()
    assert replay_file.exists()
    assert Path(str(evidence_file) + ".completion.json").exists()
    
    # 5. Test replay success
    res_replay = replay(str(replay_file), str(evidence_file))
    assert res_replay.get("ok") is True
    assert res_replay.get("verified") is True
    
    # 6. Test replay failure on mutated evidence
    lines = evidence_file.read_text().splitlines()
    # Mutate tool name in one of the events
    mutated_lines = [line.replace("fixture.echo", "malicious.tool") for line in lines]
    evidence_file.write_text("\n".join(mutated_lines) + "\n")
    
    res_replay_fail = replay(str(replay_file), str(evidence_file))
    assert res_replay_fail.get("contract_name") == "error-envelope"
    assert res_replay_fail.get("error_code") == "REPLAY_VERIFICATION_FAILED"
