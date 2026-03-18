import argparse
import os
import subprocess
from typing import List


def _read_designs(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def _normalize_path(path: str) -> str:
    return os.path.abspath(path).replace("\\", "/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert generated Verilog to BENCH AIG using yosys")
    parser.add_argument("--verilog-dir", required=True, help="Directory containing generated Verilog files")
    parser.add_argument("--home", required=True, help="Home directory containing OPENABC_DATASET")
    parser.add_argument("--designs-file", help="Optional designs.txt to limit conversion")
    parser.add_argument("--yosys", default="yosys", help="Path to yosys binary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verilog_dir = os.path.abspath(args.verilog_dir)
    out_root = os.path.join(os.path.abspath(args.home), "OPENABC_DATASET", "bench")
    os.makedirs(out_root, exist_ok=True)

    if args.designs_file:
        logic_ids = _read_designs(args.designs_file)
        verilog_files = [os.path.join(verilog_dir, f"{logic_id}.v") for logic_id in logic_ids]
    else:
        verilog_files = [
            os.path.join(verilog_dir, name)
            for name in os.listdir(verilog_dir)
            if name.endswith(".v")
        ]
        logic_ids = [os.path.splitext(os.path.basename(p))[0] for p in verilog_files]

    for logic_id, verilog_path in zip(logic_ids, verilog_files):
        if not os.path.exists(verilog_path):
            raise FileNotFoundError(f"Missing Verilog file: {verilog_path}")
        module_name = f"design_{logic_id}"
        out_dir = os.path.join(out_root, logic_id)
        os.makedirs(out_dir, exist_ok=True)
        out_bench = os.path.join(out_dir, f"{logic_id}_orig.bench")

        verilog_norm = _normalize_path(verilog_path)
        bench_norm = _normalize_path(out_bench)

        script = (
            f"read_verilog \"{verilog_norm}\"; "
            f"synth -top {module_name}; "
            f"abc -g AND; "
            f"write_bench \"{bench_norm}\""
        )
        subprocess.run([args.yosys, "-p", script], check=True)


if __name__ == "__main__":
    main()
