#!/usr/bin/env node
'use strict'
/**
 * Basic tests for awesome-skill-forge JS package.
 * Run: node tests/test_js.js
 */

const path = require('path')
const { load, search, listSkills, categories, sources, stats } = require(path.join(__dirname, '..', 'js', 'src', 'index.js'))

let passed = 0
let failed = 0

function assert (condition, label) {
  if (condition) {
    console.log(`  ✅ ${label}`)
    passed++
  } else {
    console.error(`  ❌ ${label}`)
    failed++
  }
}

function assertThrows (fn, label) {
  try {
    fn()
    console.error(`  ❌ ${label} (expected error, got none)`)
    failed++
  } catch {
    console.log(`  ✅ ${label}`)
    passed++
  }
}

console.log('\n── stats ──')
const s = stats()
assert(typeof s === 'object', 'stats returns object')
assert(s.total > 90000, `total > 90k (got ${s.total})`)
assert(s.withContent >= 160, `withContent >= 160 (got ${s.withContent})`)
assert('ClawHub' in s.bySource, 'bySource includes ClawHub')
assert('built-in' in s.bySource, 'bySource includes built-in')

console.log('\n── search ──')
const r1 = search('github')
assert(Array.isArray(r1), 'search returns array')
const r2 = search('code', { limit: 5 })
assert(r2.length <= 5, 'respects limit')
const r3 = search('docker', { limit: 1 })
assert(r3.length > 0 && 'name' in r3[0], 'result has name field')
const r4 = search('agent', { source: 'built-in', limit: 10 })
assert(r4.every(r => r.source === 'built-in'), 'filter by source works')
const r5 = search('xyzzy_nonexistent_12345')
assert(r5.length === 0, 'no results returns empty array')

console.log('\n── load ──')
const skill1 = load('github-pr-workflow')
assert(skill1 && skill1.name, 'load returns skill')
assert(skill1.prompt.length > 200, 'official skill has content')
assert(skill1.source === 'built-in', 'correct source')
assert(skill1.toString() === skill1.prompt, 'toString returns prompt')
assertThrows(() => load('xyzzy-not-a-skill'), 'not found throws error')

const skill2 = load('docker-management')
assert(skill2.source === 'optional', 'optional skill loads')

const skill3 = load('ethsmith')
assert(skill3.source === 'lord1egypt', 'lord1egypt skill loads')
assert(skill3.author === 'Lord1Egypt', 'correct author')

console.log('\n── listSkills ──')
const list1 = listSkills({ limit: 10 })
assert(list1.length <= 10, 'listSkills respects limit')
const list2 = listSkills({ source: 'built-in', limit: 100 })
assert(list2.every(r => r.source === 'built-in'), 'listSkills filter by source')

console.log('\n── categories / sources ──')
const cats = categories()
assert(typeof cats === 'object' && Object.keys(cats).length > 5, 'categories returns dict')
const srcs = sources()
assert('ClawHub' in srcs && 'built-in' in srcs, 'sources has expected keys')

console.log(`\n${'─'.repeat(40)}`)
console.log(`Results: ${passed} passed, ${failed} failed`)
if (failed > 0) process.exit(1)
