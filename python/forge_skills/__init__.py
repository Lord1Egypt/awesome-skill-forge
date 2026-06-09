"""
forge-skills: 90,000+ universal AI agent skills for any LLM framework.

Works with Claude Code, OpenAI Agents, Hermes Agent, AutoGen, LangChain, and any LLM.

Usage:
    from forge_skills import load, search, list_skills, categories, sources, stats

    skill = load("github-pr-workflow")
    print(skill.prompt)

    # Fetch community skill content on demand (requires internet)
    skill = load("aso-playbook", fetch=True)
    print(skill.prompt)

    results = search("data analysis")
    print(results[0]["name"])
"""

from .loader import load, search, list_skills, categories, sources, stats, Skill

__version__ = "1.0.4"
__all__ = ["load", "search", "list_skills", "categories", "sources", "stats", "Skill"]
