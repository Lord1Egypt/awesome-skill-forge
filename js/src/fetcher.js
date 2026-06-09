'use strict'
/**
 * On-demand content fetcher for community skills.
 * Zero dependencies — uses Node.js built-in https module.
 */

const https = require('https')
const http = require('http')
const zlib = require('zlib')
const { URL } = require('url')

const CLAWHUB_API = 'https://clawhub.ai/api/v1'
const LOBEHUB_RAW = 'https://raw.githubusercontent.com/lobehub/lobe-chat-agents/main/src'
const GITHUB_API = 'https://api.github.com'
const TOKEN = process.env.GITHUB_TOKEN || ''

function ghHeaders () {
  const h = { 'User-Agent': 'awesome-skill-forge/1.0' }
  if (TOKEN) {
    h.Authorization = `Bearer ${TOKEN}`
    h.Accept = 'application/vnd.github+json'
  }
  return h
}

function get (url, opts = {}) {
  return new Promise((resolve) => {
    const parsed = new URL(url)
    const mod = parsed.protocol === 'https:' ? https : http
    const headers = opts.github ? ghHeaders() : { 'User-Agent': 'awesome-skill-forge/1.0' }
    const req = mod.get(url, { headers, timeout: opts.timeout || 20000 }, (res) => {
      const chunks = []
      res.on('data', c => chunks.push(c))
      res.on('end', () => {
        const buf = Buffer.concat(chunks)
        if (opts.binary) return resolve(buf)
        resolve(buf.toString('utf8'))
      })
    })
    req.on('error', () => resolve(null))
    req.on('timeout', () => { req.destroy(); resolve(null) })
  })
}

async function getJson (url, opts = {}) {
  const raw = await get(url, opts)
  if (!raw) return null
  try { return JSON.parse(raw) } catch { return null }
}

async function githubFile (repo, path) {
  const url = `${GITHUB_API}/repos/${repo}/contents/${encodeURIComponent(path)}`
  const data = await getJson(url, { github: true })
  if (!data || typeof data !== 'object') return null
  if (data.encoding === 'base64' && data.content) {
    return Buffer.from(data.content.replace(/\n/g, ''), 'base64').toString('utf8')
  }
  if (data.download_url) return get(data.download_url, { github: true })
  return null
}

async function fetchClawhub (slug) {
  const meta = await getJson(`${CLAWHUB_API}/skills/${slug}`)
  if (!meta) return null
  const skill = meta.skill || meta
  const lv = meta.latestVersion || skill.latestVersion
  let version = null
  if (lv && typeof lv === 'object') version = lv.version
  if (!version && skill.tags) {
    version = typeof skill.tags === 'object' ? skill.tags.latest : null
  }
  if (!version) return null

  const raw = await get(
    `${CLAWHUB_API}/download?slug=${slug}&version=${encodeURIComponent(String(version))}`,
    { binary: true, timeout: 40000 }
  )
  if (!raw) return null

  // Parse ZIP in-memory using basic ZIP format reading
  // Node doesn't have built-in ZIP, but we can try to extract SKILL.md
  // by finding its content in the buffer
  try {
    // Find "SKILL.md" signature in ZIP
    const marker = Buffer.from('SKILL.md')
    let pos = raw.indexOf(marker)
    while (pos !== -1) {
      // Local file header: signature 0x04034b50, then offsets to find data
      // Search backwards for PK header (0x504B0304)
      const pkPos = raw.lastIndexOf(Buffer.from([0x50, 0x4B, 0x03, 0x04]), pos)
      if (pkPos !== -1) {
        const compMethod = raw.readUInt16LE(pkPos + 8)
        const compSize = raw.readUInt32LE(pkPos + 18)
        const fnLen = raw.readUInt16LE(pkPos + 26)
        const extraLen = raw.readUInt16LE(pkPos + 28)
        const dataStart = pkPos + 30 + fnLen + extraLen
        const compData = raw.slice(dataStart, dataStart + compSize)
        if (compMethod === 0) {
          return compData.toString('utf8')
        } else if (compMethod === 8) {
          try {
            return zlib.inflateRawSync(compData).toString('utf8')
          } catch { /* try next */ }
        }
      }
      pos = raw.indexOf(marker, pos + 1)
    }
  } catch { /* fall through */ }
  return null
}

async function fetchLobehub (identifier) {
  const agentId = identifier.split('/').pop()
  const data = await getJson(`${LOBEHUB_RAW}/${agentId}.json`)
  if (!data) return null
  const cfg = data.config || {}
  const meta = data.meta || {}
  const body = (cfg.systemRole || '').trim()
  if (!body) return null
  const title = meta.title || agentId
  const desc = meta.description || ''
  const tags = (meta.tags || []).join(', ')
  return `---\nname: ${agentId}\ndescription: "${desc}"\nsource: LobeHub\ntags: [${tags}]\ncompatible: [claude-code, openai-agents, hermes-agent, any-llm]\n---\n\n# ${title}\n\n${body}\n`
}

async function fetchSkillsSh (identifier) {
  const ident = identifier.replace(/^skills[-_]sh\//, '')
  const parts = ident.split('/')
  if (parts.length < 3) return null
  const repo = `${parts[0]}/${parts[1]}`
  const skill = parts.slice(2).join('/')
  const candidates = [
    `skills/${skill}/SKILL.md`,
    `.agents/skills/${skill}/SKILL.md`,
    `${skill}/SKILL.md`,
    `plugins/${parts[1]}-claude/skills/${skill}/SKILL.md`,
    `src/${skill}/SKILL.md`
  ]
  for (const path of candidates) {
    const content = await githubFile(repo, path)
    if (content && content.length > 80) return content
  }
  return null
}

async function fetchGstack (sourceUrl) {
  const m = sourceUrl.match(/https:\/\/github\.com\/([^/]+\/[^/]+)\/tree\/[^/]+\/(.+)/)
  if (!m) return null
  return githubFile(m[1], `${m[2].replace(/\/$/, '')}/SKILL.md`)
}

/**
 * Fetch full SKILL.md content for a community skill on demand.
 * @param {Object} meta - Skill metadata from index
 * @returns {Promise<string|null>}
 */
async function fetchContent (meta) {
  const source = meta.source || ''
  const identifier = meta.identifier || meta.localPath || ''
  const sourceUrl = meta.sourceUrl || ''

  if (source === 'ClawHub') {
    const slug = identifier.split('/').pop()
    return fetchClawhub(slug)
  }
  if (source === 'LobeHub') return fetchLobehub(identifier)
  if (source === 'skills.sh') return fetchSkillsSh(identifier)
  if (source === 'gstack') return fetchGstack(sourceUrl)
  return null
}

module.exports = { fetchContent }
