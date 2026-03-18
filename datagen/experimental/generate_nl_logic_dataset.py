import argparse
import hashlib
import json
import os
import random
import urllib.error
import urllib.request
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

VN_USE_CASE_TEMPLATES = {
    "and": [
        "dùng làm tín hiệu enable khi cả a và b cùng bật",
    ],
    "or": [
        "kích hoạt báo động nếu a hoặc b bật",
    ],
    "xor": [
        "phát hiện a và b khác nhau",
    ],
    "nand": [
        "tạo tín hiệu active-low khi cả a và b đều 1",
    ],
    "nor": [
        "tạo tín hiệu active-low khi bất kỳ ngõ vào nào bật",
    ],
    "not": [
        "đảo mức để tạo tín hiệu active-low từ a",
    ],
    "mux2": [
        "chọn một trong hai nguồn dữ liệu {w} bit cho bus ra",
    ],
    "mux4": [
        "chọn một trong bốn kênh dữ liệu {w} bit",
    ],
    "decoder2": [
        "giải mã địa chỉ 2 bit để bật 1 trong 4 thiết bị",
    ],
    "decoder3": [
        "giải mã địa chỉ 3 bit để bật 1 trong 8 thiết bị",
    ],
    "encoder4": [
        "mã hóa 4 tín hiệu one-hot thành chỉ số 2 bit",
    ],
    "encoder8": [
        "mã hóa 8 tín hiệu one-hot thành chỉ số 3 bit",
    ],
    "half_adder": [
        "tính tổng 1 bit trong mạch đếm đơn giản",
    ],
    "full_adder": [
        "tính tổng 1 bit với carry trong bộ cộng",
    ],
    "ripple_adder": [
        "cộng hai số {w} bit trong datapath",
    ],
    "cmp_eq": [
        "so sánh hai số {w} bit để kiểm tra bằng nhau",
    ],
    "cmp_gt": [
        "kiểm tra số {w} bit a lớn hơn b",
    ],
    "cmp_lt": [
        "kiểm tra số {w} bit a nhỏ hơn b",
    ],
}

EN_USE_CASE_TEMPLATES = {
    "and": [
        "use as enable when both a and b are true",
    ],
    "or": [
        "trigger an alarm if a or b is high",
    ],
    "xor": [
        "detect whether a and b differ",
    ],
    "nand": [
        "generate active-low when both a and b are 1",
    ],
    "nor": [
        "generate active-low when any input is high",
    ],
    "not": [
        "invert a to create an active-low control",
    ],
    "mux2": [
        "select one of two {w}-bit data sources for output",
    ],
    "mux4": [
        "select one of four {w}-bit channels",
    ],
    "decoder2": [
        "decode a 2-bit address to enable 1 of 4 devices",
    ],
    "decoder3": [
        "decode a 3-bit address to enable 1 of 8 devices",
    ],
    "encoder4": [
        "encode 4 one-hot inputs into a 2-bit index",
    ],
    "encoder8": [
        "encode 8 one-hot inputs into a 3-bit index",
    ],
    "half_adder": [
        "compute a 1-bit sum in a simple counter",
    ],
    "full_adder": [
        "compute a 1-bit sum with carry in an adder",
    ],
    "ripple_adder": [
        "add two {w}-bit values in the datapath",
    ],
    "cmp_eq": [
        "check equality of two {w}-bit values",
    ],
    "cmp_gt": [
        "check whether a {w}-bit value a is greater than b",
    ],
    "cmp_lt": [
        "check whether a {w}-bit value a is less than b",
    ],
}

VN_SPEC_LONG_TEMPLATE = """Hãy tạo một module Verilog thuần combinational circuit (không dùng clock, không dùng reg cho output trừ khi cần always @*).

Yêu cầu:
- Tên module: {module_name}
- Inputs: {inputs_desc}
- Outputs: {outputs_desc}
- Chức năng: {function_desc}

Hãy viết code theo kiểu:
- Sử dụng assign cho các biểu thức đơn giản
- Hoặc always @(*) với if/case cho logic phức tạp hơn
- Phải là purely combinational (không có latch, không có combinatorial loop)
- Thêm comment giải thích từng phần
- Module phải có tên chính xác, port list rõ ràng
- Không cần testbench trừ khi tôi yêu cầu sau"""

EN_SPEC_LONG_TEMPLATE = """Please create a purely combinational Verilog module (no clock, no output reg unless always @* is needed).

Requirements:
- Module name: {module_name}
- Inputs: {inputs_desc}
- Outputs: {outputs_desc}
- Function: {function_desc}

Please write the code as:
- Use assign for simple expressions
- Or always @(*) with if/case for more complex logic
- Must be purely combinational (no latch, no combinational loop)
- Add comments explaining each part
- Module name and port list must be exact
- No testbench unless I ask later"""


def _parse_csv(text: str) -> List[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def _normalize_lmstudio_endpoint(endpoint: str) -> str:
    endpoint = endpoint.strip().rstrip("/")
    if endpoint.endswith("/chat/completions"):
        return endpoint
    if endpoint.endswith("/v1"):
        return f"{endpoint}/chat/completions"
    return f"{endpoint}/v1/chat/completions"


def _lmstudio_models_endpoint(endpoint: str) -> str:
    chat_endpoint = _normalize_lmstudio_endpoint(endpoint)
    return chat_endpoint[: -len("/chat/completions")] + "/models"


def _extract_chat_content(response_json: Dict) -> Optional[str]:
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    message = choices[0].get("message", {})
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        merged = "".join(text_parts).strip()
        return merged if merged else None
    return None


def _detect_lmstudio_model(endpoint: str, timeout_sec: int, api_key: Optional[str] = None) -> str:
    models_endpoint = _lmstudio_models_endpoint(endpoint)
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(models_endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LM Studio model discovery failed (HTTP {exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LM Studio model discovery failed: {exc}") from exc

    models = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(models, list) or not models:
        raise RuntimeError("LM Studio returned no loaded models at /v1/models")

    first_id = models[0].get("id")
    if not isinstance(first_id, str) or not first_id.strip():
        raise RuntimeError("LM Studio model list does not contain a valid model id")
    return first_id.strip()


def _rewrite_prompt_text_lmstudio(
    text: str,
    lang: str,
    style: str,
    endpoint: str,
    model: str,
    timeout_sec: int,
    min_chars: int,
    max_chars: int,
    api_key: Optional[str] = None,
) -> str:
    chat_endpoint = _normalize_lmstudio_endpoint(endpoint)
    system_text = (
        "You rewrite prompts for Verilog code generation. "
        "Preserve technical meaning and required constraints."
    )
    user_text = (
        f"Rewrite this prompt in language '{lang}' and keep style '{style}'.\n"
        f"Target length: {min_chars}-{max_chars} characters (medium length).\n"
        "Rules:\n"
        "- Keep module name exactly unchanged if present.\n"
        "- Keep function/logic intent unchanged.\n"
        "- Keep combinational-only requirement if present.\n"
        "- Keep concise and remove repetition.\n"
        "- Return only the rewritten prompt text.\n\n"
        f"Original prompt:\n{text}"
    )
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(
        chat_endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            response_json = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LM Studio rewrite failed (HTTP {exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LM Studio rewrite failed: {exc}") from exc

    rewritten = _extract_chat_content(response_json)
    if not rewritten:
        raise RuntimeError("LM Studio returned empty rewrite content")
    return rewritten


def _style_target_range(style: str, min_chars: int, max_chars: int) -> Tuple[int, int]:
    if style == "spec":
        return max(20, min_chars // 2), max(80, min(max_chars, 120))
    if style == "use_case":
        return max(30, min_chars), max(100, min(max_chars, 160))
    if style == "spec_long":
        return max(90, min_chars + 40), max(180, min(max_chars + 60, 320))
    return min_chars, max_chars


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


def _inputs_desc(inputs: List[str]) -> str:
    if not inputs:
        return "(none)"
    return ", ".join([f"input {name}" for name in inputs])


def _outputs_desc(outputs: List[str]) -> str:
    if not outputs:
        return "(none)"
    return ", ".join([f"output {name}" for name in outputs])


def _function_desc(family: str, width: int) -> str:
    if family == "and":
        return "y = a AND b"
    if family == "or":
        return "y = a OR b"
    if family == "xor":
        return "y = a XOR b"
    if family == "nand":
        return "y = NOT(a AND b)"
    if family == "nor":
        return "y = NOT(a OR b)"
    if family == "not":
        return "y = NOT a"
    if family == "mux2":
        return "y = (s==0)? d0 : d1, each bit independently"
    if family == "mux4":
        return "y selects one of d0,d1,d2,d3 by s1,s0, each bit independently"
    if family == "decoder2":
        return "y0..y3 one-hot decode of a1,a0"
    if family == "decoder3":
        return "y0..y7 one-hot decode of a2,a1,a0"
    if family == "encoder4":
        return "encode one-hot d0..d3 to y[1:0]"
    if family == "encoder8":
        return "encode one-hot d0..d7 to y[2:0]"
    if family == "half_adder":
        return "sum = a XOR b, cout = a AND b"
    if family == "full_adder":
        return "sum = a XOR b XOR cin, cout = majority(a,b,cin)"
    if family == "ripple_adder":
        return f"add two {width}-bit numbers a and b, outputs sum[0..{width-1}] and cout"
    if family == "cmp_eq":
        return f"y = 1 if a == b for {width}-bit inputs"
    if family == "cmp_gt":
        return f"y = 1 if a > b for {width}-bit inputs"
    if family == "cmp_lt":
        return f"y = 1 if a < b for {width}-bit inputs"
    return "implement the specified logic"


def _prompt_variants(
    family: str,
    width: int,
    inputs: List[str],
    outputs: List[str],
    logic_id: str,
    include_spec_long: bool = True,
) -> List[Dict[str, str]]:
    prompts = []
    for tmpl in VN_TEMPLATES.get(family, []):
        prompts.append({"lang": "vi", "text": tmpl.format(w=width), "style": "spec"})
    for tmpl in EN_TEMPLATES.get(family, []):
        prompts.append({"lang": "en", "text": tmpl.format(w=width), "style": "spec"})
    for tmpl in VN_USE_CASE_TEMPLATES.get(family, []):
        prompts.append({"lang": "vi", "text": tmpl.format(w=width), "style": "use_case"})
    for tmpl in EN_USE_CASE_TEMPLATES.get(family, []):
        prompts.append({"lang": "en", "text": tmpl.format(w=width), "style": "use_case"})

    if include_spec_long:
        module_name = f"design_{logic_id}"
        inputs_desc = _inputs_desc(inputs)
        outputs_desc = _outputs_desc(outputs)
        function_desc = _function_desc(family, width)
        prompts.append({
            "lang": "vi",
            "text": VN_SPEC_LONG_TEMPLATE.format(
                module_name=module_name,
                inputs_desc=inputs_desc,
                outputs_desc=outputs_desc,
                function_desc=function_desc,
            ),
            "style": "spec_long",
        })
        prompts.append({
            "lang": "en",
            "text": EN_SPEC_LONG_TEMPLATE.format(
                module_name=module_name,
                inputs_desc=inputs_desc,
                outputs_desc=outputs_desc,
                function_desc=function_desc,
            ),
            "style": "spec_long",
        })
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


def _gen_comparators(max_width: int) -> List[LogicSpec]:
    specs = []
    for w in range(1, max_width + 1):
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


def generate_dataset(
    out_dir: str,
    total: int,
    seed: int,
    lmstudio_endpoint: Optional[str] = None,
    lmstudio_model: Optional[str] = None,
    lmstudio_timeout_sec: int = 60,
    rewrite_styles: Optional[List[str]] = None,
    min_prompt_chars: int = 40,
    max_prompt_chars: int = 180,
    lmstudio_api_key: Optional[str] = None,
    include_spec_long: bool = True,
) -> None:
    random.seed(seed)
    all_specs = []
    all_specs.extend(_gen_basic_gates())
    all_specs.extend(_gen_muxes(list(range(1, 9))))
    all_specs.extend(_gen_decoders())
    all_specs.extend(_gen_encoders())
    all_specs.extend(_gen_adders())

    # Scale comparator width so the candidate pool is large enough for the requested total.
    # Each comparator width contributes 3 specs: cmp_eq, cmp_gt, cmp_lt.
    non_comparator_count = len(all_specs)
    needed_comparator_specs = max(0, total - non_comparator_count)
    comparator_max_width = max(8, (needed_comparator_specs + 2) // 3)
    all_specs.extend(_gen_comparators(comparator_max_width))

    all_specs = _validate_specs(all_specs)
    if len(all_specs) < total:
        raise ValueError(
            f"Unable to generate {total} unique designs; only {len(all_specs)} available."
        )

    rewrite_enabled = bool(lmstudio_endpoint)
    rewrite_style_set = set(rewrite_styles or [])
    resolved_model = lmstudio_model
    if rewrite_enabled and not resolved_model:
        resolved_model = _detect_lmstudio_model(
            lmstudio_endpoint,
            lmstudio_timeout_sec,
            lmstudio_api_key,
        )

    rewrite_successes = 0
    rewrite_failures = 0

    random.shuffle(all_specs)
    selected = all_specs[:total]

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
            }, ensure_ascii=False) + "\n")

            for prompt in _prompt_variants(
                spec.family,
                spec.width,
                spec.inputs,
                spec.outputs,
                spec.logic_id,
                include_spec_long=include_spec_long,
            ):
                text = prompt["text"]
                if rewrite_enabled and prompt["style"] in rewrite_style_set:
                    style_min, style_max = _style_target_range(
                        prompt["style"],
                        min_prompt_chars,
                        max_prompt_chars,
                    )
                    try:
                        rewritten = _rewrite_prompt_text_lmstudio(
                            text=text,
                            lang=prompt["lang"],
                            style=prompt["style"],
                            endpoint=lmstudio_endpoint,
                            model=resolved_model,
                            timeout_sec=lmstudio_timeout_sec,
                            min_chars=style_min,
                            max_chars=style_max,
                            api_key=lmstudio_api_key,
                        )
                        text = rewritten
                        rewrite_successes += 1
                    except RuntimeError:
                        rewrite_failures += 1

                prompt_f.write(json.dumps({
                    "logic_id": spec.logic_id,
                    "lang": prompt["lang"],
                    "style": prompt["style"],
                    "text": text,
                }, ensure_ascii=False) + "\n")

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

    if rewrite_enabled:
        print(
            f"LM Studio rewrite summary: success={rewrite_successes}, failed={rewrite_failures}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate NL→logic dataset with Verilog outputs")
    parser.add_argument("--out", required=True, help="Output directory (e.g., datasets/nl_verilog)")
    parser.add_argument("--total", type=int, default=200, help="Total number of designs to generate")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    parser.add_argument(
        "--lmstudio-endpoint",
        default="",
        help="LM Studio OpenAI-compatible endpoint (e.g., http://127.0.0.1:1234)",
    )
    parser.add_argument(
        "--lmstudio-model",
        default="",
        help="Model id for LM Studio. If omitted, auto-detect from /v1/models",
    )
    parser.add_argument(
        "--lmstudio-timeout-sec",
        type=int,
        default=60,
        help="Timeout for each LM Studio request in seconds",
    )
    parser.add_argument(
        "--rewrite-styles",
        default="spec,use_case",
        help="Comma-separated styles to rewrite via LM Studio",
    )
    parser.add_argument(
        "--min-prompt-chars",
        type=int,
        default=40,
        help="Minimum target chars for rewritten prompts",
    )
    parser.add_argument(
        "--max-prompt-chars",
        type=int,
        default=180,
        help="Maximum target chars for rewritten prompts",
    )
    parser.add_argument(
        "--lmstudio-api-key",
        default="",
        help="Optional Bearer token for LM Studio compatible API",
    )
    parser.add_argument(
        "--include-spec-long",
        action="store_true",
        help="Include spec_long prompts (disabled by default)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rewrite_styles = _parse_csv(args.rewrite_styles)
    lmstudio_endpoint = args.lmstudio_endpoint.strip() or None
    lmstudio_model = args.lmstudio_model.strip() or None
    lmstudio_api_key = args.lmstudio_api_key.strip() or None
    generate_dataset(
        out_dir=args.out,
        total=args.total,
        seed=args.seed,
        lmstudio_endpoint=lmstudio_endpoint,
        lmstudio_model=lmstudio_model,
        lmstudio_timeout_sec=args.lmstudio_timeout_sec,
        rewrite_styles=rewrite_styles,
        min_prompt_chars=args.min_prompt_chars,
        max_prompt_chars=args.max_prompt_chars,
        lmstudio_api_key=lmstudio_api_key,
        include_spec_long=args.include_spec_long,
    )


if __name__ == "__main__":
    main()
