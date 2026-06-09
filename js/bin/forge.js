#!/usr/bin/env node
'use strict'

const { load, search, listSkills, categories, sources, stats } = require('../src/index')

const args = process.argv.slice(2)
const cmd = args[0]

function parseFlags (args) {
  const flags = {}
  let i = 0
  while (i < args.length) {
    if (args[i] === '--category' || args[i] === '-c') {
      flags.category = args[++i]
    } else if (args[i] === '--source' || args[i] === '-s') {
      flags.source = args[++i]
    } else if (args[i] === '--limit' || args[i] === '-n') {
      flags.limit = parseInt(args[++i])
    } else if (args[i] === '--content-only') {
      flags.hasContent = true
    } else if (args[i] === '--json') {
      flags.json = true
    }
    i++
  }
  return flags
}

function printSkillRow (r) {
  const flag = r.hasContent ? '[+]' : '[ ]'
  const src = (r.source || '').padEnd(12)
  const cat = (r.category || '').padEnd(20)
  console.log(`  ${flag} ${r.name.padEnd(40)} ${src} ${cat}`)
}

switch (cmd) {
  case 'stats': {
    const s = stats()
    console.log('\n forge-skills Index Stats')
    console.log(`  Total skills:      ${s.total.toLocaleString()}`)
    console.log(`  With content:      ${s.withContent.toLocaleString()}`)
    console.log(`  Format:            ${s.format}`)
    console.log('  Compatible:        Claude Code, OpenAI Agents, Hermes, AutoGen, LangChain, any LLM')
    console.log('\n  Top Sources:')
    Object.entries(s.bySource).slice(0, 8).forEach(([k, v]) =>
      console.log(`    ${k.padEnd(20)} ${v.toLocaleString().padStart(8)}`))
    console.log('\n  Top Categories:')
    Object.entries(s.byCategory).slice(0, 8).forEach(([k, v]) =>
      console.log(`    ${k.padEnd(25)} ${v.toLocaleString().padStart(8)}`))
    console.log()
    break
  }

  case 'search': {
    const query = args[1]
    if (!query) { console.error('Usage: forge search <query>'); process.exit(1) }
    const flags = parseFlags(args.slice(2))
    const results = search(query, flags)
    if (!results.length) { console.log(`No results for '${query}'`); break }
    console.log(`\n  Results for '${query}' (${results.length} found):\n`)
    results.forEach(r => {
      printSkillRow(r)
      if (r.description) console.log(`           ${r.description.slice(0, 90)}`)
      console.log()
    })
    break
  }

  case 'list': {
    const flags = parseFlags(args.slice(1))
    const results = listSkills(flags)
    if (!results.length) { console.log('No skills found.'); break }
    console.log(`\n  Skills (${results.length} shown):\n`)
    results.forEach(printSkillRow)
    console.log()
    break
  }

  case 'load': {
    const name = args[1]
    if (!name) { console.error('Usage: forge load <skill-name>'); process.exit(1) }
    const flags = parseFlags(args.slice(2))
    try {
      const skill = load(name, flags)
      if (flags.json) {
        console.log(JSON.stringify({
          name: skill.name, description: skill.description,
          category: skill.category, source: skill.source,
          compatible: skill.compatible, prompt: skill.prompt
        }, null, 2))
      } else {
        console.log(`\n  Skill: ${skill.name}`)
        console.log(`  Category: ${skill.category}  |  Source: ${skill.source}  |  Author: ${skill.author}`)
        console.log(`  Compatible: ${skill.compatible.join(', ')}`)
        if (skill.sourceUrl) console.log(`  Source URL: ${skill.sourceUrl}`)
        console.log('\n' + '='.repeat(60) + '\n')
        console.log(skill.prompt)
        console.log()
      }
    } catch (e) {
      console.error(e.message); process.exit(1)
    }
    break
  }

  case 'sources': {
    const s = sources()
    console.log('\n  Skill Sources:\n')
    Object.entries(s).forEach(([k, v]) =>
      console.log(`  ${k.padEnd(25)} ${v.toLocaleString().padStart(8)} skills`))
    console.log()
    break
  }

  case 'categories': {
    const c = categories()
    console.log('\n  Skill Categories:\n')
    Object.entries(c).slice(0, 30).forEach(([k, v]) =>
      console.log(`  ${k.padEnd(30)} ${v.toLocaleString().padStart(8)} skills`))
    console.log()
    break
  }

  default:
    console.log(`
  forge-skills CLI — 90k+ universal AI agent skills

  Commands:
    forge stats                          Index statistics
    forge search <query> [--category X]  Search skills
    forge list [--source X] [--category X] [--content-only]
    forge load <name> [--json]           Load and display a skill
    forge sources                        List source registries
    forge categories                     List categories

  Examples:
    forge stats
    forge search "github pr"
    forge search "agent" --category ai-agents
    forge list --source built-in --content-only
    forge load github-pr-workflow
    npx forge-skills stats
`)
}
