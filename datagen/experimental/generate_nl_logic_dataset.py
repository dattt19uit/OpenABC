import argparse
import hashlib
import json
import os
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class LogicSpec:
    logic_id: str
    family: str
    width: int
    inputs: List[str]
    outputs: List[str]
    expr_map: Dict[str, str]
    meta: Dict[str, str]


GATE_TEMPLATES = [
    ("and", "a & b"),
    ("or", "a | b"),
    ("xor", "a ^ b"),
    ("nand", "~(a & b)"),
    ("nor", "~(a | b)"),
]

VN_TEMPLATES = {
    "and": [
        "tạo mạch AND 1 bit với ngõ vào a,b",
        "thiết kế cổng AND cho a và b",
    ],
    "or": [
        "tạo mạch OR 1 bit với ngõ vào a,b",
        "thiết kế cổng OR cho a và b",
    ],
    "xor": [
        "tạo mạch XOR 1 bit với ngõ vào a,b",
        "thiết kế cổng XOR cho a và b",
    ],
    "nand": [
        "tạo mạch NAND 1 bit với ngõ vào a,b",
        "thiết kế cổng NAND cho a và b",
    ],
    "nor": [
        "tạo mạch NOR 1 bit với ngõ vào a,b",
        "thiết kế cổng NOR cho a và b",
    ],
    "not": [
        "tạo mạch NOT 1 bit với ngõ vào a",
        "thiết kế cổng đảo cho a",
    ],
    "mux2": [
        "tạo mux 2:1 {w} bit chọn giữa d0,d1 với s",
        "thiết kế bộ chọn 2:1 {w} bit với ngõ chọn s",
    ],
    "mux4": [
        "tạo mux 4:1 {w} bit chọn giữa d0..d3 với s1,s0",
        "thiết kế bộ chọn 4:1 {w} bit với 2 bit chọn",
    ],
    "decoder2": [
        "tạo bộ giải mã 2->4 với ngõ vào a1,a0",
        "thiết kế decoder 2 sang 4",
    ],
    "decoder3": [
        "tạo bộ giải mã 3->8 với ngõ vào a2,a1,a0",
        "thiết kế decoder 3 sang 8",
    ],
    "encoder4": [
        "tạo bộ mã hóa 4->2 một hot",
        "thiết kế encoder 4 vào 2 ra",
    ],
    "encoder8": [
        "tạo bộ mã hóa 8->3 một hot",
        "thiết kế encoder 8 vào 3 ra",
    ],
    "half_adder": [
        "tạo mạch nửa cộng với a,b",
        "thiết kế half adder 1 bit",
    ],
    "full_adder": [
        "tạo mạch toàn cộng với a,b,cin",
        "thiết kế full adder 1 bit",
    ],
    "ripple_adder": [
        "tạo bộ cộng ripple {w} bit",
        "thiết kế bộ cộng {w} bit",
    ],
    "cmp_eq": [
        "so sánh bằng cho hai số {w} bit",
        "thiết kế comparator bằng {w} bit",
    ],
    "cmp_gt": [
        "so sánh lớn hơn cho hai số {w} bit",
        "thiết kế comparator > {w} bit",
    ],
    "cmp_lt": [
        "so sánh nhỏ hơn cho hai số {w} bit",
        "thiết kế comparator < {w} bit",
    ],
}

EN_TEMPLATES = {
    "and": [
        "build a 1-bit AND gate with inputs a,b",
        "design AND for a and b",
    ],
    "or": [
        "build a 1-bit OR gate with inputs a,b",
        "design OR for a and b",
    ],
    "xor": [
        "build a 1-bit XOR gate with inputs a,b",
        "design XOR for a and b",
    ],
    "nand": [
        "build a 1-bit NAND gate with inputs a,b",
        "design NAND for a and b",
    ],
    "nor": [
        "build a 1-bit NOR gate with inputs a,b",
        "design NOR for a and b",
    ],
    "not": [
        "build a 1-bit NOT gate with input a",
        "design inverter for a",
    ],
    "mux2": [
        "build a {w}-bit 2:1 mux selecting d0,d1 with s",
        "design a {w}-bit 2:1 multiplexer with select s",
    ],
    "mux4": [
        "build a {w}-bit 4:1 mux selecting d0..d3 with s1,s0",
        "design a {w}-bit 4:1 multiplexer with 2-bit select",
    ],
    "decoder2": [
        "build a 2-to-4 decoder with inputs a1,a0",
        "design decoder 2 to 4",
    ],
    "decoder3": [
        "build a 3-to-8 decoder with inputs a2,a1,a0",
        "design decoder 3 to 8",
    ],
    "encoder4": [
        "build a 4-to-2 one-hot encoder",
        "design encoder 4 in 2 out",
    ],
    "encoder8": [
        "build an 8-to-3 one-hot encoder",
        "design encoder 8 in 3 out",
    ],
    "half_adder": [
        "build a half adder with a,b",
        "design a 1-bit half adder",
    ],
    "full_adder": [
        "build a full adder with a,b,cin",
        "design a 1-bit full adder",
    ],
    "ripple_adder": [
        "build a {w}-bit ripple adder",
        "design a {w}-bit adder",
    ],
    "cmp_eq": [
        "compare equality for two {w}-bit numbers",
        "design {w}-bit equality comparator",
    ],
    "cmp_gt": [
        "compare greater-than for two {w}-bit numbers",
        "design {w}-bit greater-than comparator",
    ],
    "cmp_lt": [
        "compare less-than for two {w}-bit numbers",
        "design {w}-bit less-than comparator",
    ],
}


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _logic_id(family: str, width: int, expr_map: Dict[str, str]) -> str:
    payload = json.dumps({"family": family, "width": width, "expr": expr_map}, sort_keys=True)
    return f"{family}_{width}_{_hash_text(payload)}"


def _bits(prefix: str, width: int) -> List[str]:
    return [f"{prefix}{i}" for i in range(width)]


def _mux2_expr(d0: str, d1: str, s: str) -> str:
    return f"(({d0} & ~{s}) | ({d1} & {s}))"


def _mux4_expr(d: List[str], s1: str, s0: str) -> str:
    t0 = f"({d[0]} & ~{s1} & ~{s0})"
    t1 = f"({d[1]} & ~{s1} & {s0})"
    t2 = f"({d[2]} & {s1} & ~{s0})"
    t3 = f"({d[3]} & {s1} & {s0})"
    return f"({t0} | {t1} | {t2} | {t3})"


def _decoder_expr(inputs: List[str]) -> List[str]:
    width = len(inputs)
    outputs = []
    for i in range(2 ** width):
        terms = []
        for bit in range(width):
            if (i >> bit) & 1:
                terms.append(inputs[bit])
            else:
                terms.append(f"~{inputs[bit]}")
        outputs.append(" & ".join(terms))
    return outputs


def _encoder_expr(inputs: List[str], out_width: int) -> List[str]:
    outputs = []
    for bit in range(out_width):
        terms = []
        for i, inp in enumerate(inputs):
            if (i >> bit) & 1:
                terms.append(inp)
        outputs.append(" | ".join(terms) if terms else "0")
    return outputs


def _half_adder_expr(a: str, b: str) -> Tuple[str, str]:
    return f"({a} ^ {b})", f"({a} & {b})"


def _full_adder_expr(a: str, b: str, cin: str) -> Tuple[str, str]:
    sum_expr = f"({a} ^ {b} ^ {cin})"
    carry_expr = f"(({a} & {b}) | ({a} & {cin}) | ({b} & {cin}))"
    return sum_expr, carry_expr


def _ripple_adder_expr(a_bits: List[str], b_bits: List[str]) -> Tuple[List[str], str]:
    carry = "0"
    sums = []
    for a, b in zip(a_bits, b_bits):
        s, c = _full_adder_expr(a, b, carry)
        sums.append(s)
        carry = c
    return sums, carry


def _cmp_eq_expr(a_bits: List[str], b_bits: List[str]) -> str:
    terms = [f"~({a} ^ {b})" for a, b in zip(a_bits, b_bits)]
    return " & ".join(terms)


def _cmp_gt_lt_expr(a_bits: List[str], b_bits: List[str], mode: str) -> str:
    # mode: 'gt' or 'lt'
    n = len(a_bits)
    cmp_terms = []
    for i in reversed(range(n)):
        ai = a_bits[i]
        bi = b_bits[i]
        higher_equal_terms = []
        for j in range(i + 1, n):
            higher_equal_terms.append(f"~({a_bits[j]} ^ {b_bits[j]})")
        prefix = " & ".join(higher_equal_terms) if higher_equal_terms else "1"
        if mode == "gt":
            cmp_terms.append(f"({prefix} & {ai} & ~{bi})")
        else:
            cmp_terms.append(f"({prefix} & ~{ai} & {bi})")
    return " | ".join(cmp_terms) if cmp_terms else "0"


def _evaluate_expr(expr: str, env: Dict[str, int]) -> int:
    expr_eval = expr.replace("~", "1-")
    return 1 if eval(expr_eval, {"__builtins__": {}}, env) == 1 else 0


MAX_TRUTH_INPUTS = 8


def _truth_table(expr_map: Dict[str, str], inputs: List[str]) -> Optional[str]:
    if len(inputs) > MAX_TRUTH_INPUTS:
        return None
    table = []
    for mask in range(2 ** len(inputs)):
        env = {inputs[i]: (mask >> i) & 1 for i in range(len(inputs))}
        outputs = []
        for name in sorted(expr_map.keys()):
            outputs.append(_evaluate_expr(expr_map[name], env))
        table.append("".join(str(v) for v in outputs))
    return "|".join(table)


def _logic_to_verilog(spec: LogicSpec) -> str:
    module_name = f"design_{spec.logic_id}"
    ports = [p for p in spec.inputs + spec.outputs]
    lines = [f"module {module_name}({', '.join(ports)});"]
    if spec.inputs:
        lines.append(f"  input {', '.join(spec.inputs)};")
    if spec.outputs:
        lines.append(f"  output {', '.join(spec.outputs)};")
    for out in spec.outputs:
        lines.append(f"  assign {out} = {spec.expr_map[out]};")
    lines.append("endmodule")
    return "\n".join(lines)


def _prompt_variants(family: str, width: int) -> List[Dict[str, str]]:
    prompts = []
    for tmpl in VN_TEMPLATES.get(family, []):
        prompts.append({"lang": "vi", "text": tmpl.format(w=width)})
    for tmpl in EN_TEMPLATES.get(family, []):
        prompts.append({"lang": "en", "text": tmpl.format(w=width)})
    return prompts


def _gen_basic_gates() -> List[LogicSpec]:
    specs = []
    inputs = ["a", "b"]
    for name, expr in GATE_TEMPLATES:
        spec = LogicSpec(
            logic_id="",
            family=name,
            width=1,
            inputs=inputs,
            outputs=["y"],
            expr_map={"y": expr},
            meta={"gate": name},
        )
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)
    # NOT gate
    spec = LogicSpec(
        logic_id="",
        family="not",
        width=1,
        inputs=["a"],
        outputs=["y"],
        expr_map={"y": "~a"},
        meta={"gate": "not"},
    )
    spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
    specs.append(spec)
    return specs


def _gen_muxes(widths: List[int]) -> List[LogicSpec]:
    specs = []
    for w in widths:
        d0 = _bits("d0_", w)
        d1 = _bits("d1_", w)
        s = "s"
        expr_map = {}
        for i in range(w):
            expr_map[f"y{i}"] = _mux2_expr(d0[i], d1[i], s)
        inputs = d0 + d1 + [s]
        outputs = [f"y{i}" for i in range(w)]
        spec = LogicSpec("", "mux2", w, inputs, outputs, expr_map, {"kind": "2to1"})
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)

        d = [
            _bits("d0_", w),
            _bits("d1_", w),
            _bits("d2_", w),
            _bits("d3_", w),
        ]
        s1, s0 = "s1", "s0"
        expr_map = {}
        for i in range(w):
            expr_map[f"y{i}"] = _mux4_expr([d[0][i], d[1][i], d[2][i], d[3][i]], s1, s0)
        inputs = d[0] + d[1] + d[2] + d[3] + [s1, s0]
        outputs = [f"y{i}" for i in range(w)]
        spec = LogicSpec("", "mux4", w, inputs, outputs, expr_map, {"kind": "4to1"})
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)
    return specs


def _gen_decoders() -> List[LogicSpec]:
    specs = []
    for width in [2, 3]:
        ins = _bits("a", width)
        out_exprs = _decoder_expr(ins)
        expr_map = {f"y{i}": out_exprs[i] for i in range(len(out_exprs))}
        spec = LogicSpec(
            "", f"decoder{width}", width, ins, list(expr_map.keys()), expr_map, {}
        )
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)
    return specs


def _gen_encoders() -> List[LogicSpec]:
    specs = []
    configs = [(4, 2), (8, 3)]
    for in_w, out_w in configs:
        ins = _bits("d", in_w)
        out_exprs = _encoder_expr(ins, out_w)
        expr_map = {f"y{i}": out_exprs[i] for i in range(out_w)}
        spec = LogicSpec(
            "", f"encoder{in_w}", in_w, ins, list(expr_map.keys()), expr_map, {}
        )
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)
    return specs


def _gen_adders() -> List[LogicSpec]:
    specs = []
    # half adder
    s, c = _half_adder_expr("a", "b")
    spec = LogicSpec("", "half_adder", 1, ["a", "b"], ["sum", "cout"], {"sum": s, "cout": c}, {})
    spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
    specs.append(spec)
    # full adder
    s, c = _full_adder_expr("a", "b", "cin")
    spec = LogicSpec("", "full_adder", 1, ["a", "b", "cin"], ["sum", "cout"], {"sum": s, "cout": c}, {})
    spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
    specs.append(spec)
    # ripple adders
    for w in [2, 3, 4, 5, 6, 7, 8]:
        a_bits = _bits("a", w)
        b_bits = _bits("b", w)
        sums, cout = _ripple_adder_expr(a_bits, b_bits)
        expr_map = {f"sum{i}": sums[i] for i in range(w)}
        expr_map["cout"] = cout
        inputs = a_bits + b_bits
        outputs = [f"sum{i}" for i in range(w)] + ["cout"]
        spec = LogicSpec("", "ripple_adder", w, inputs, outputs, expr_map, {})
        spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
        specs.append(spec)
    return specs


def _gen_comparators() -> List[LogicSpec]:
    specs = []
    for w in range(1, 9):
        a_bits = _bits("a", w)
        b_bits = _bits("b", w)
        eq_expr = _cmp_eq_expr(a_bits, b_bits)
        gt_expr = _cmp_gt_lt_expr(a_bits, b_bits, "gt")
        lt_expr = _cmp_gt_lt_expr(a_bits, b_bits, "lt")
        for family, expr in [("cmp_eq", eq_expr), ("cmp_gt", gt_expr), ("cmp_lt", lt_expr)]:
            spec = LogicSpec("", family, w, a_bits + b_bits, ["y"], {"y": expr}, {})
            spec.logic_id = _logic_id(spec.family, spec.width, spec.expr_map)
            specs.append(spec)
    return specs


def _validate_specs(specs: List[LogicSpec]) -> List[LogicSpec]:
    seen = {}
    valid = []
    for spec in specs:
        table = _truth_table(spec.expr_map, spec.inputs)
        if table is None:
            valid.append(spec)
            continue
        if table in seen:
            continue
        seen[table] = spec.logic_id
        valid.append(spec)
    return valid


def generate_dataset(out_dir: str, total: int, seed: int) -> None:
    random.seed(seed)
    all_specs = []
    all_specs.extend(_gen_basic_gates())
    all_specs.extend(_gen_muxes(list(range(1, 9))))
    all_specs.extend(_gen_decoders())
    all_specs.extend(_gen_encoders())
    all_specs.extend(_gen_adders())
    all_specs.extend(_gen_comparators())
    all_specs = _validate_specs(all_specs)

    random.shuffle(all_specs)
    selected = all_specs[: min(total, len(all_specs))]

    os.makedirs(out_dir, exist_ok=True)
    verilog_dir = os.path.join(out_dir, "verilog")
    os.makedirs(verilog_dir, exist_ok=True)

    logic_path = os.path.join(out_dir, "logic.jsonl")
    prompts_path = os.path.join(out_dir, "prompts.jsonl")
    manifest_path = os.path.join(out_dir, "manifest.jsonl")
    designs_path = os.path.join(out_dir, "designs.txt")

    with open(logic_path, "w", encoding="utf-8") as logic_f, \
        open(prompts_path, "w", encoding="utf-8") as prompt_f, \
        open(manifest_path, "w", encoding="utf-8") as manifest_f, \
        open(designs_path, "w", encoding="utf-8") as designs_f:
        for spec in selected:
            logic_f.write(json.dumps({
                "logic_id": spec.logic_id,
                "family": spec.family,
                "width": spec.width,
                "inputs": spec.inputs,
                "outputs": spec.outputs,
                "expr_map": spec.expr_map,
                "meta": spec.meta,
            }) + "\n")

            for prompt in _prompt_variants(spec.family, spec.width):
                prompt_f.write(json.dumps({
                    "logic_id": spec.logic_id,
                    "lang": prompt["lang"],
                    "text": prompt["text"],
                }) + "\n")

            verilog = _logic_to_verilog(spec)
            verilog_file = os.path.join(verilog_dir, f"{spec.logic_id}.v")
            with open(verilog_file, "w", encoding="utf-8") as vf:
                vf.write(verilog + "\n")

            manifest_f.write(json.dumps({
                "logic_id": spec.logic_id,
                "family": spec.family,
                "width": spec.width,
                "verilog": verilog_file,
            }) + "\n")

            designs_f.write(spec.logic_id + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate NL→logic dataset with Verilog outputs")
    parser.add_argument("--out", required=True, help="Output directory (e.g., datasets/nl_verilog)")
    parser.add_argument("--total", type=int, default=200, help="Total number of designs to generate")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_dataset(args.out, args.total, args.seed)


if __name__ == "__main__":
    main()
