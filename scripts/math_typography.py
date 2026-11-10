"""Typeset the diagrams' inline mathematical notation with Matplotlib mathtext.

Chinese prose stays in the CJK font. Existing $...$ expressions are preserved;
plain mathematical runs are translated to the same Computer Modern math font.
"""
from __future__ import annotations

import re

_SUPER = str.maketrans({"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+", "ᵗ": "t", "ⁱ": "i", "ʲ": "j", "ᵏ": "k"})
_SUB = str.maketrans({"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9", "ᵢ": "i", "ⱼ": "j", "ₖ": "k", "₊": "+", "₋": "-", "₌": "="})
_SUPER_CHARS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ᵗⁱʲᵏ"
_SUB_CHARS = "₀₁₂₃₄₅₆₇₈₉ᵢⱼₖ₊₋₌"
_SYMBOLS = {
    "λ": r"\lambda ", "Δ": r"\Delta ", "β": r"\beta ",
    "Φ": r"\Phi ", "ψ": r"\psi ", "χ": r"\chi ", "Σ": r"\sum ",
    "−": "-", "×": r"\times ", "∩": r"\cap ", "⊕": r"\oplus ",
    "←": r"\leftarrow ", "≠": r"\ne ", "⊆": r"\subseteq ",
    "±": r"\pm ", "〈": r"\langle ", "〉": r"\rangle ",
    "′": r"^{\prime}", "ᵀ": r"^{\mathsf{T}}", "{": r"\{", "}": r"\}",
}
_CHARS = r"A-Za-z0-9_\s=+\-*/.,:;()\[\]{}|<>λΔβΦψχΣ−×∩⊕←≠⊆±〈〉′ᵀ" + _SUPER_CHARS + _SUB_CHARS
_RUN = re.compile("[" + _CHARS.replace(r"\s", " ") + "]+")
_MATRIX = re.compile(r"\[\[([^\[\]]+)\],\[([^\[\]]+)\]\]")
_OPERATOR = re.compile(r"(?<![A-Za-z])(nullity|rank|span|diag|gcd|lcm|det|ker|dim)(?![A-Za-z])")


def _math_fragment(value: str, allow_matrix: bool = True) -> str:
    result = []
    i = 0
    while i < len(value):
        if allow_matrix:
            match = _MATRIX.match(value, i)
            if match:
                rows = [r"\quad ".join(_math_fragment(cell.strip(), False)
                                        for cell in row.split(","))
                        for row in match.groups()]
                result.append(r"\left[\genfrac{}{}{0}{}{" + rows[0] + "}{" + rows[1] + r"}\right]")
                i = match.end()
                continue
        match = _OPERATOR.match(value, i)
        if match:
            result.append(r"\mathrm{" + match.group() + "}")
            i = match.end()
            continue
        c = value[i]
        if c in _SUPER_CHARS or c in _SUB_CHARS:
            chars = _SUPER_CHARS if c in _SUPER_CHARS else _SUB_CHARS
            translation = _SUPER if c in _SUPER_CHARS else _SUB
            end = i + 1
            while end < len(value) and value[end] in chars:
                end += 1
            result.append(("^{" if c in _SUPER_CHARS else "_{") + value[i:end].translate(translation) + "}")
            i = end
            continue
        result.append(_SYMBOLS.get(c, c))
        i += 1
    return "".join(result)


def _convert_run(match: re.Match[str]) -> str:
    run = match.group()
    stripped = run.strip()
    if not stripped or not re.search(r"[A-Za-z0-9λΔβΦψχΣ]", stripped):
        return run
    # Keep punctuation and surrounding spaces in the prose font, outside math.
    core = stripped.strip(" ,.:;")
    if not core or (core.isascii() and core.isalpha() and len(core) > 2):
        return run
    start = run.index(core)
    end = start + len(core)
    return run[:start] + "$" + _math_fragment(core) + "$" + run[end:]


def typeset_inline(text: str) -> str:
    """Preserve authored math and turn plain inline expressions into mathtext."""
    parts = re.split(r"(\$[^$]*\$)", text)
    for i in range(0, len(parts), 2):
        parts[i] = _RUN.sub(_convert_run, parts[i])
    return "".join(parts)
