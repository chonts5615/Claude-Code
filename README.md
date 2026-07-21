# Claude-Code

A monorepo of Cargill HR / talent-management tooling plus tools for **Bloom
Beauty Suites & Lash Bar**. It bundles installable Python apps, standalone Claude
Skills, and a Claude Code **plugin marketplace**. See [`CLAUDE.md`](./CLAUDE.md)
for the full map.

## Claude Code plugin marketplace

Two installable plugins live under [`plugins/`](./plugins) (registered by
[`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json)):

- **`cargill-io-psych`** — I-O-psychology skills for talent assessment, job
  analysis, assessment-center design, career architecture, and adverse-impact
  analysis.
- **`bloom-beauty-ops`** — salon operations skills: marketing, booking,
  pricing/financials, and hiring.

Install from any Claude Code session:

```
/plugin marketplace add chonts5615/Claude-Code
/plugin install cargill-io-psych@cargill-bloom-suite
/plugin install bloom-beauty-ops@cargill-bloom-suite
```

See [`plugins/README.md`](./plugins/README.md) for details.
