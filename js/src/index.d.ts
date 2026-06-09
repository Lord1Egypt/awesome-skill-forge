export interface SkillMeta {
  name: string;
  description: string;
  category: string;
  tags: string[];
  platforms: string[];
  author: string;
  version: string;
  license: string;
  source: string;
  sourceUrl: string;
  compatible: string[];
  hasContent: boolean;
  localPath?: string;
}

export interface Skill extends SkillMeta {
  prompt: string;
  toString(): string;
}

export interface LoadOptions {
  category?: string;
  source?: string;
}

export interface SearchOptions {
  category?: string;
  source?: string;
  limit?: number;
  hasContent?: boolean;
}

export interface ListOptions {
  category?: string;
  source?: string;
  hasContent?: boolean;
  limit?: number;
}

export interface Stats {
  total: number;
  withContent: number;
  bySource: Record<string, number>;
  byCategory: Record<string, number>;
  format: string;
  version: string;
}

export function load(name: string, opts?: LoadOptions): Skill;
export function search(query: string, opts?: SearchOptions): SkillMeta[];
export function listSkills(opts?: ListOptions): SkillMeta[];
export function categories(): Record<string, number>;
export function sources(): Record<string, number>;
export function stats(): Stats;
