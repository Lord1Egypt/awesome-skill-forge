"""
forge-skills CLI: search, load, list, and stats.

Usage:
    forge stats
    forge search "data analysis"
    forge search "agent" --category ai-agents --source built-in
    forge list --category productivity --content-only
    forge load github-pr-workflow
    forge sources
    forge categories
"""

import argparse
import sys
import json

from .loader import load, search, list_skills, categories, sources, stats


def cmd_stats(args):
    s = stats()
    print(f"\n forge-skills Index Stats")
    print(f"  Total skills:      {s['total']:,}")
    print(f"  With content:      {s['with_content']:,}")
    print(f"  Format:            {s['format']}")
    print(f"  Compatible with:   Claude Code, OpenAI Agents, Hermes, AutoGen, LangChain, any LLM")
    print(f"\n  Top Sources:")
    for src, count in list(s["by_source"].items())[:10]:
        print(f"    {src:<20} {count:>8,}")
    print(f"\n  Top Categories:")
    for cat, count in list(s["by_category"].items())[:10]:
        print(f"    {cat:<25} {count:>8,}")
    print()


def cmd_search(args):
    results = search(
        args.query,
        category=args.category,
        source=args.source,
        limit=args.limit,
        has_content=True if args.content_only else None,
    )
    if not results:
        print(f"No results for '{args.query}'")
        return
    print(f"\n  Results for '{args.query}' ({len(results)} found):\n")
    for r in results:
        content_flag = "[content]" if r.get("hasContent") else "[ref]"
        print(f"  {content_flag}  {r['name']:<40}  {r.get('source',''):>12}  {r.get('category','')}")
        if r.get("description"):
            print(f"           {r['description'][:90]}")
        print()


def cmd_list(args):
    results = list_skills(
        category=args.category,
        source=args.source,
        has_content=True if args.content_only else None,
        limit=args.limit,
    )
    if not results:
        print("No skills found with those filters.")
        return
    print(f"\n  Skills ({len(results)} shown):\n")
    for r in results:
        content_flag = "[+]" if r.get("hasContent") else "[ ]"
        print(f"  {content_flag} {r['name']:<40}  {r.get('source',''):>12}  {r.get('category','')}")
    print()


def cmd_load(args):
    try:
        skill = load(args.name, category=args.category, source=args.source)
    except KeyError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.json:
        print(json.dumps({
            "name": skill.name,
            "description": skill.description,
            "category": skill.category,
            "source": skill.source,
            "compatible": skill.compatible,
            "prompt": skill.prompt,
        }, indent=2, ensure_ascii=False))
        return

    print(f"\n  Skill: {skill.name}")
    print(f"  Category: {skill.category}  |  Source: {skill.source}  |  Author: {skill.author}")
    print(f"  Compatible: {', '.join(skill.compatible)}")
    if skill.source_url:
        print(f"  Source URL: {skill.source_url}")
    print(f"\n{'='*60}\n")
    print(skill.prompt)
    print()


def cmd_sources(args):
    s = sources()
    print(f"\n  Skill Sources:\n")
    for src, count in s.items():
        print(f"  {src:<25} {count:>8,} skills")
    print()


def cmd_categories(args):
    c = categories()
    print(f"\n  Skill Categories:\n")
    for cat, count in c.items():
        print(f"  {cat:<30} {count:>8,} skills")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="forge",
        description="forge-skills: 90k+ universal AI agent skills",
    )
    sub = parser.add_subparsers(dest="command")

    # stats
    sub.add_parser("stats", help="Show index statistics")

    # search
    p_search = sub.add_parser("search", help="Search skills by keyword")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--category", "-c", help="Filter by category")
    p_search.add_argument("--source", "-s", help="Filter by source")
    p_search.add_argument("--limit", "-n", type=int, default=10)
    p_search.add_argument("--content-only", action="store_true", help="Only skills with local content")

    # list
    p_list = sub.add_parser("list", help="List skills")
    p_list.add_argument("--category", "-c", help="Filter by category")
    p_list.add_argument("--source", "-s", help="Filter by source")
    p_list.add_argument("--limit", "-n", type=int, default=50)
    p_list.add_argument("--content-only", action="store_true")

    # load
    p_load = sub.add_parser("load", help="Load and display a skill")
    p_load.add_argument("name", help="Skill name")
    p_load.add_argument("--category", "-c")
    p_load.add_argument("--source", "-s")
    p_load.add_argument("--json", action="store_true", help="Output as JSON")

    # sources
    sub.add_parser("sources", help="Show skill counts by source registry")

    # categories
    sub.add_parser("categories", help="Show skill counts by category")

    args = parser.parse_args()

    commands = {
        "stats": cmd_stats,
        "search": cmd_search,
        "list": cmd_list,
        "load": cmd_load,
        "sources": cmd_sources,
        "categories": cmd_categories,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
