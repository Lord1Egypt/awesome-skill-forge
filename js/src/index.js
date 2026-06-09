'use strict'
/**
 * awesome-skill-forge: 90,000+ universal AI agent skills.
 * Works with Claude Code, OpenAI Agents, Hermes, AutoGen, LangChain, any LLM.
 *
 * @example
 * const { load, search, listSkills, categories } = require('awesome-skill-forge')
 * const skill = await load('github-pr-workflow')
 * console.log(skill.prompt)
 *
 * // Fetch community skill content on demand (requires internet)
 * const skill = await load('aso-playbook', { fetch: true })
 * console.log(skill.prompt)
 */

const fs = require('fs')
const path = require('path')
const { fetchContent } = require('./fetcher')

// Resolve index.json — works installed or from project root
let INDEX_PATH = path.join(__dirname, '..', 'data', 'index.json')
if (!fs.existsSync(INDEX_PATH)) {
  INDEX_PATH = path.join(__dirname, '..', '..', 'index.json')
}

let _indexCache = null

function loadIndex () {
  if (!_indexCache) {
    const raw = fs.readFileSync(INDEX_PATH, 'utf8')
    _indexCache = JSON.parse(raw)
  }
  return _indexCache
}

function readSkillContent (meta) {
  // Embedded content (pre-loaded in index.json for official skills)
  if (meta.content) return meta.content

  const localPath = meta.localPath || ''
  if (!localPath) return meta.description || ''

  const bases = [
    path.join(__dirname, '..'),
    path.join(__dirname, '..', '..')
  ]
  for (const base of bases) {
    const skillMd = path.join(base, localPath, 'SKILL.md')
    if (fs.existsSync(skillMd)) {
      const raw = fs.readFileSync(skillMd, 'utf8')
      const bodyMatch = raw.match(/^---\n[\s\S]*?\n---\n([\s\S]*)/)
      return bodyMatch ? bodyMatch[1].trim() : raw
    }
  }
  return meta.description || ''
}

/**
 * A loaded skill object.
 * @typedef {Object} Skill
 * @property {string} name
 * @property {string} description
 * @property {string} category
 * @property {string[]} tags
 * @property {string[]} platforms
 * @property {string} author
 * @property {string} version
 * @property {string} license
 * @property {string} source
 * @property {string} sourceUrl
 * @property {string[]} compatible
 * @property {boolean} hasContent
 * @property {string} prompt - Full skill content
 */

/**
 * Load a skill by name. Returns a Promise when fetch:true, otherwise synchronous.
 * @param {string} name - Skill name (case-insensitive)
 * @param {Object} [opts]
 * @param {string} [opts.category] - Filter by category
 * @param {string} [opts.source] - Filter by source
 * @param {boolean} [opts.fetch] - Fetch content from source API if not embedded (requires internet)
 * @returns {Skill|Promise<Skill>}
 */
function load (name, opts = {}) {
  const index = loadIndex()
  const nameLower = name.toLowerCase()
  const { category, source, fetch: doFetch } = opts

  for (const meta of index.skills) {
    if (meta.name.toLowerCase() !== nameLower) continue
    if (category && meta.category?.toLowerCase() !== category.toLowerCase()) continue
    if (source && meta.source?.toLowerCase() !== source.toLowerCase()) continue

    const makeSkill = (content) => ({
      name: meta.name,
      description: meta.description || '',
      category: meta.category || '',
      tags: meta.tags || [],
      platforms: meta.platforms || [],
      author: meta.author || 'community',
      version: meta.version || '1.0.0',
      license: meta.license || 'MIT',
      source: meta.source || '',
      sourceUrl: meta.sourceUrl || '',
      compatible: meta.compatible || [],
      hasContent: !!meta.hasContent,
      localPath: meta.localPath || '',
      prompt: content,
      toString () { return this.prompt }
    })

    if (meta.hasContent) {
      return makeSkill(readSkillContent(meta))
    }

    if (doFetch) {
      return fetchContent(meta).then(fetched => makeSkill(fetched || meta.description || ''))
    }

    return makeSkill(meta.description || '')
  }

  throw new Error(`Skill not found: '${name}'`)
}

/**
 * Search skills by keyword.
 * @param {string} query
 * @param {Object} [opts]
 * @param {string} [opts.category]
 * @param {string} [opts.source]
 * @param {number} [opts.limit=10]
 * @param {boolean} [opts.hasContent] - Only skills with local content
 * @returns {Object[]} Array of skill metadata
 */
function search (query, opts = {}) {
  const index = loadIndex()
  const { category, source, limit = 10, hasContent } = opts
  const q = query.toLowerCase()
  const results = []

  for (const meta of index.skills) {
    if (category && meta.category?.toLowerCase() !== category.toLowerCase()) continue
    if (source && meta.source?.toLowerCase() !== source.toLowerCase()) continue
    if (hasContent !== undefined && !!meta.hasContent !== hasContent) continue

    let score = 0
    if (meta.name?.toLowerCase().includes(q)) score += 10
    if (meta.description?.toLowerCase().includes(q)) score += 5
    if ((meta.tags || []).join(' ').toLowerCase().includes(q)) score += 3

    if (score > 0) results.push({ score, meta })
  }

  results.sort((a, b) => b.score - a.score)
  return results.slice(0, limit).map(r => r.meta)
}

/**
 * List skills with optional filters.
 * @param {Object} [opts]
 * @param {string} [opts.category]
 * @param {string} [opts.source]
 * @param {boolean} [opts.hasContent]
 * @param {number} [opts.limit=100]
 * @returns {Object[]}
 */
function listSkills (opts = {}) {
  const index = loadIndex()
  const { category, source, hasContent, limit = 100 } = opts
  const results = []

  for (const meta of index.skills) {
    if (category && meta.category?.toLowerCase() !== category.toLowerCase()) continue
    if (source && meta.source?.toLowerCase() !== source.toLowerCase()) continue
    if (hasContent !== undefined && !!meta.hasContent !== hasContent) continue
    results.push(meta)
    if (results.length >= limit) break
  }

  return results
}

/**
 * Get skill counts per category.
 * @returns {Object} { category: count }
 */
function categories () {
  const index = loadIndex()
  return index.byCategory || {}
}

/**
 * Get skill counts per source registry.
 * @returns {Object} { source: count }
 */
function sources () {
  const index = loadIndex()
  return index.bySource || {}
}

/**
 * Get overall index statistics.
 * @returns {Object}
 */
function stats () {
  const index = loadIndex()
  return {
    total: index.totalSkills || 0,
    withContent: index.skillsWithContent || 0,
    bySource: sources(),
    byCategory: categories(),
    format: index.format || '',
    version: index.version || ''
  }
}

module.exports = { load, search, listSkills, categories, sources, stats }
