"""Command-line entry point: new / status / run / resume.

Usage (from the repository root):
    PYTHONPATH=framework python3 -m engine new <product> [--desc "one-line request"]
    PYTHONPATH=framework python3 -m engine status <product>
    PYTHONPATH=framework python3 -m engine run <product> [--max N] [--approve-release] [--driver manual|claude]
    PYTHONPATH=framework python3 -m engine resume <product>
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

from .driver import ManualDriver
from .runner import run
from .state import State


def _make_driver(name: str):
    """Create a driver by name: manual = offline; claude = Claude Agent SDK (needs an API key)."""
    if name == "claude":
        from .driver import ClaudeAgentDriver
        return ClaudeAgentDriver()
    return ManualDriver()

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS = ROOT / "products"
TEMPLATE = PRODUCTS / "_template"


def _product_dir(name: str) -> Path:
    return PRODUCTS / name


def cmd_new(args) -> int:
    dst = _product_dir(args.name)
    if dst.exists():
        print(f"error: product already exists: {dst}", file=sys.stderr)
        return 1
    dst.mkdir(parents=True)
    today = _dt.date.today().isoformat()
    # copy PROJECT.md and sdd-state.json from the template and fill in the placeholders
    for fn in ("PROJECT.md", "sdd-state.json"):
        text = (TEMPLATE / fn).read_text(encoding="utf-8")
        text = text.replace("<product-name>", args.name).replace("<YYYY-MM-DD>", today)
        if fn == "PROJECT.md" and args.desc:
            text = text.replace("<one-line description of what this product does>", args.desc)
        (dst / fn).write_text(text, encoding="utf-8")
    (dst / "activity-log.md").write_text(f"# Activity log · {args.name}\n\n", encoding="utf-8")
    st = State.load(dst / "sdd-state.json")
    st.log("0-bootstrap", "orchestrator", f"Created product '{args.name}', mode={st.data.get('mode')}")
    st.save()
    print(f"Created product: products/{args.name}/")
    print(f"Next: PYTHONPATH=framework python3 -m engine run {args.name}")
    return 0


def cmd_status(args) -> int:
    p = _product_dir(args.name) / "sdd-state.json"
    if not p.exists():
        print(f"error: product not found: {args.name}", file=sys.stderr)
        return 1
    st = State.load(p)
    print(f"Product: {st.product}   mode: {st.data.get('mode')}   budget: {st.budget_str()}")
    print(f"Current stage: {st.data.get('current_stage')}")
    print("-" * 52)
    for sid in st.stage_order:
        s = st.stages[sid]
        mark = {"done": "✓", "in_progress": "…", "pending": " "}.get(s.get("status"), "?")
        gate = "human" if s.get("gate") == "human" else "auto"
        print(f" [{mark}] {sid:16} gate={gate:5}  role={s.get('agent','-')}")
    last = st.data.get("activity", {}).get("last_entry")
    if last:
        print("-" * 52)
        print("Last activity: " + last)
    return 0


def cmd_run(args) -> int:
    p = _product_dir(args.name) / "sdd-state.json"
    if not p.exists():
        print(f"error: product not found: {args.name}", file=sys.stderr)
        return 1
    st = State.load(p)
    reason = run(st, driver=_make_driver(getattr(args, "driver", "manual")),
                 approve_release=getattr(args, "approve_release", False),
                 max_steps=getattr(args, "max", None))
    print(f"\nRun finished: {reason}")
    if reason == "completed":
        print("All stages completed.")
    elif reason == "paused:human-gate":
        print("Reached the release-preview gate. After previewing and approving, run:")
        print(f"  PYTHONPATH=framework python3 -m engine run {args.name} --approve-release")
    elif reason.startswith("paused:budget"):
        print("Budget exhausted. Raise budget.max_steps in sdd-state.json, then resume.")
    else:
        print("Once the missing artifacts are produced, continue with:")
        print(f"  PYTHONPATH=framework python3 -m engine resume {args.name}")
    print(f"Details: products/{args.name}/activity-log.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engine", description="Autonomous development production-line engine")
    sub = parser.add_subparsers(dest="command")

    pn = sub.add_parser("new", help="create a product")
    pn.add_argument("name")
    pn.add_argument("--desc", default=None)
    pn.set_defaults(func=cmd_new)

    ps = sub.add_parser("status", help="show progress")
    ps.add_argument("name")
    ps.set_defaults(func=cmd_status)

    for cname, helptext in (("run", "advance the production line"), ("resume", "continue from the last pause")):
        pr = sub.add_parser(cname, help=helptext)
        pr.add_argument("name")
        pr.add_argument("--max", type=int, default=None, help="maximum number of steps in this run")
        pr.add_argument("--approve-release", action="store_true", help="approve the release preview and pass the human gate")
        pr.add_argument("--driver", choices=["manual", "claude"], default="manual",
                        help="manual = offline (default); claude = produce artifacts with the Claude Agent SDK (needs an API key)")
        pr.set_defaults(func=cmd_run)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
