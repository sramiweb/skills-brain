#!/usr/bin/env python3
"""Skills Brain CLI v2 - Interface unifiee pour tooling"""
import argparse
import sys
from pathlib import Path

def cmd_validate(args):
    from validate import validate_all_skills
    print("Running validation...\n")
    validate_all_skills()

def cmd_catalog(args):
    from catalog import generate_catalog
    print("Generating catalog...\n")
    generate_catalog()

def cmd_evaluate(args):
    from evaluator import evaluate_all_skills
    print("Running evaluation...\n")
    evaluate_all_skills()

def cmd_resolve(args):
    from resolver import resolve_capabilities
    caps = args.caps if args.caps else ["deployment.orchestration", "security.scanning"]
    print(f"Resolving capabilities: {caps}\n")
    resolve_capabilities(caps)

def cmd_run_all(args):
    print("Running full pipeline: validate -> catalog -> evaluate\n")
    cmd_validate(args)
    print()
    cmd_catalog(args)
    print()
    cmd_evaluate(args)

def main():
    parser = argparse.ArgumentParser(prog="skills-brain", description="Skills Brain CLI v2")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    p_validate = subparsers.add_parser("validate", help="Validate all skills")
    p_validate.set_defaults(func=cmd_validate)
    
    p_catalog = subparsers.add_parser("catalog", help="Generate catalog")
    p_catalog.set_defaults(func=cmd_catalog)
    
    p_evaluate = subparsers.add_parser("evaluate", help="Evaluate skills (Q0-Q5)")
    p_evaluate.set_defaults(func=cmd_evaluate)
    
    p_resolve = subparsers.add_parser("resolve", help="Resolve capabilities")
    p_resolve.add_argument("caps", nargs="*", help="Capabilities")
    p_resolve.set_defaults(func=cmd_resolve)
    
    p_all = subparsers.add_parser("run-all", help="Run full pipeline")
    p_all.set_defaults(func=cmd_run_all)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == "__main__":
    main()
