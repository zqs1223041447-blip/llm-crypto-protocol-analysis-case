"""Call local scyther-w32.exe with binary stdout (Windows-safe)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_text(element: ET.Element, path: str) -> str | None:
    node = element.find(path)
    return node.text if node is not None else None


def parse_claims(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    claims = []
    for node in root.findall("claimstatus"):
        claim_type = first_text(node, "./claimtype/const") or "unknown"
        label = first_text(node, "./label/tuple/op2/const") or first_text(node, "./label/const") or "unknown"
        protocol = first_text(node, "./protocol/const") or "unknown"
        role_node = node.find("./role/var")
        role = role_node.attrib.get("name", "unknown") if role_node is not None else "unknown"
        failed = int(first_text(node, "./failed") or "0")
        count = int(first_text(node, "./count") or "0")
        states = int(first_text(node, "./states") or "0")
        complete = node.find("./complete") is not None
        if claim_type == "Reachable":
            status = "reachable" if count > 0 else "unreachable"
        elif failed > 0:
            status = "falsified"
        elif complete:
            status = "verified"
        else:
            status = "bounded"
        claims.append(
            {
                "protocol": protocol,
                "role": role,
                "label": label,
                "claim_type": claim_type,
                "status": status,
                "failed": failed,
                "count": count,
                "states": states,
                "complete": complete,
            }
        )
    return claims


def run_model(executable: Path, model: Path, output_root: Path, extra_args: list[str], timeout: int) -> dict:
    out_dir = output_root / model.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    cmd = [str(executable), "--xml-output", "--plain", *extra_args, str(model)]
    timed_out = False
    try:
        completed = subprocess.run(cmd, capture_output=True, timeout=timeout)
        stdout_b, stderr_b, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout_b = exc.stdout or b""
        stderr_b = exc.stderr or b""
        returncode = -9
    runtime = time.perf_counter() - started
    stdout = stdout_b.decode("latin-1", errors="replace")
    stderr = stderr_b.decode("latin-1", errors="replace")
    if timed_out:
        stderr = ("TIMEOUT\n" + stderr)[:8000]
    (out_dir / "result.xml").write_text(stdout, encoding="utf-8")
    (out_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    parse_success = False
    claims: list[dict] = []
    parse_error = None
    try:
        if stdout.strip().startswith("<"):
            claims = parse_claims(stdout)
            parse_success = True
    except Exception as exc:  # noqa: BLE001
        parse_error = str(exc)
    report = {
        "model": str(model),
        "model_sha256": sha256(model),
        "executable": str(executable),
        "executable_sha256": sha256(executable),
        "exit_code": returncode,
        "timed_out": timed_out,
        "command": cmd,
        "runtime_seconds": round(runtime, 3),
        "parse_success": parse_success,
        "parse_error": parse_error,
        "n_claims": len(claims),
        "claims": claims,
        "stderr_head": stderr[:2000],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", required=True)
    parser.add_argument("--models-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-runs", type=int, default=0)
    args = parser.parse_args()
    extra: list[str] = []
    if args.max_runs > 0:
        extra.extend([f"--max-runs={args.max_runs}"])
    else:
        extra.append("--unbounded")
    models = sorted(Path(args.models_dir).glob("*.spdl"))
    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    reports = [run_model(Path(args.executable), model, output_root, extra, args.timeout) for model in models]
    summary = {
        "n_models": len(reports),
        "n_parse_ok": sum(1 for r in reports if r["parse_success"]),
        "n_exit0": sum(1 for r in reports if r["exit_code"] == 0),
        "reports": [
            {
                "model": r["model"],
                "exit_code": r["exit_code"],
                "parse_success": r["parse_success"],
                "n_claims": r["n_claims"],
                "statuses": sorted({c["status"] for c in r["claims"]}),
            }
            for r in reports
        ],
    }
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
