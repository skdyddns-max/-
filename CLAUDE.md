# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this project is

Two standalone, zero-build HTML web apps for **마음터칭 (Mind Touching)**, an adult
psychological care service by **비본어게인 연담(然談)**. There is **no backend, no
bundler, no package manager, and no build step** — every file is served as-is.
Content and UI copy are in **Korean**; keep new copy Korean unless asked otherwise.

- **`index.html`** — 마음지수 진단 (Mind Index self-assessment). A mobile survey page
  linked from a brochure QR code. Users answer a short quiz, get a 0–100 score, a
  self-vs-others perception checklist, and a matched program recommendation, then
  book via a Naver form link.
- **`studio.html`** — 화용 스튜디오 (Pragmatics Studio). A single-file, offline-capable
  authoring tool that produces video-modeling content for pragmatic language therapy
  (대본 → 영상 → 음성 → 퀴즈 → 감정 카드), and exports a self-contained therapy
  "player" HTML. Installable as a PWA.

Supporting files:

- `manifest.webmanifest` — PWA manifest; `start_url` is `./studio.html`.
- `icon.svg` — app/PWA icon.
- `README.md` — user-facing Korean overview (feature-level).
- `.github/workflows/deploy-pages.yml` — GitHub Pages deploy.
- `.claude/` — Claude Code settings and the web SessionStart hook.

## Running & deploying

There is nothing to install or build. To preview locally, open the HTML files
directly or serve the repo root with any static server (e.g. `python3 -m http.server`).

**Deployment is automatic:** every push to `main` runs
`.github/workflows/deploy-pages.yml`, which uploads the repo root as the Pages
artifact and deploys it. There is no build step in CI — the deployed site is the
raw repo.

- Diagnosis page: https://skdyddns-max.github.io/-/
- Studio: https://skdyddns-max.github.io/-/studio.html

Note the repository name is literally `-`, so the Pages base path is `/-/`. Keep
asset links relative (e.g. `./studio.html`, `icon.svg`) so they resolve under that path.

## Architecture & conventions

### `index.html`
Self-contained: `<style>` block, then a `<script>` (starts ~line 451) with all logic.
Data-driven — the survey is defined by module-level constants:

- `QUESTIONS` — quiz + preference + checklist items (`type: 'scored' | 'pref' | 'checklist'`).
- `TRAITS` — trait chips for the self-vs-others checklist.
- `PROGRAMS`, `TIERS` — recommendation catalog and score tiers.
- `answers` / `pref` / `checks` — in-memory response state; `compute()` derives the score.
- Flow functions: `showScreen`, `showQuestion`, `choose`, `next`/`prev`, `finish`, `compute`.

**Booking link:** the Naver form URL is the `NAVER_FORM_URL` constant near the top of
the script (currently `""`). Set it there.

### `studio.html`
Single file with several `<style>`/`<script>` blocks. The main app logic is a
`<script type="module">` (starts ~line 414). Key pieces:

- **State model** — one module-level `state` object, persisted to `localStorage` under
  key **`pragStudio_v1`** via `save()`/`load()`. `state` holds `settings`
  (`mode`, `apiKey`, `geminiKey`, `veoModel`), the working project (`form`, `project`,
  `videos`), a multi-project library (`projects[]` of `{id, createdAt, updatedAt,
  form, project, videos}`), and `currentId`. `load()` includes migration/back-fill
  logic — preserve it when touching the state shape.
- **Navigation** — a step wizard driven by `app.go(n)`. Steps: `0` 목록(library),
  `1` 목표 설정, `2` 대본, `3` 영상 제작, `4` 퀴즈, `5` 내보내기, `7` 감정 카드,
  `6` 설정. The `app` object holds all UI handlers (referenced from inline `onclick=`).
- **Script generation** — `SYSTEM_PROMPT` + `buildUserPrompt`/`buildCopyPrompt`/
  `buildRevisePrompt`. Three engines selectable in settings: Claude API, Gemini API
  (free tier possible), or copy-prompt mode (paste into claude.ai, paste JSON back).
- **Export** — `buildPlayerHTML` generates a standalone therapy player (its own
  embedded `<style>`/`<script>`; player logs to its own `localStorage` key
  `화용플레이어기록::<title>`). `buildWorksheetHTML` generates a printable A4 worksheet.

### AI / media integrations (all client-side, keys in the user's browser only)
- **Claude** — `callClaude()` dynamically imports `@anthropic-ai/sdk` from esm.sh and
  calls `messages.create` with `model: "claude-opus-4-8"`, `dangerouslyAllowBrowser: true`,
  and a `json_schema` output config. It handles `refusal`/`max_tokens` stop reasons.
- **Gemini** (`generativelanguage.googleapis.com/v1beta`, key via `x-goog-api-key`):
  - `callGemini()` — script text, `gemini-2.5-flash`, JSON response.
  - Veo video — `state.settings.veoModel` (default `veo-3.0-fast-generate-001`;
    other options include `veo-3.0-generate-001`, `veo-3.1-*-preview`).
  - `gemini-2.5-flash-preview-tts` — Korean TTS dubbing (WAV export).
  - `gemini-2.5-flash-image` — emotion-card image generation.

When editing model IDs or API shapes, update **all** call sites and the settings UI
consistently. If you touch anything Claude/Anthropic-API-related, verify current model
IDs and API parameters rather than assuming — see the `claude-api` skill.

### Data & privacy
All user data (settings, projects, API keys, player logs) lives **only** in
`localStorage`. There is no server persistence. Preserve this — do not add network
persistence or telemetry without explicit instruction.

## Git & workflow conventions

- **Branch:** develop on `claude/claude-md-docs-auh057` for this task; create it from
  the latest `main` if needed. Never push to `main` directly — pushes to `main`
  trigger a live Pages deploy.
- **Do not open a PR unless explicitly asked.**
- **Commit messages** in this repo are written in **Korean** and describe the
  user-facing change (see `git log`), often with a PR number suffix. Match that style.
- Since a push to `main` deploys instantly, treat `main` changes as production releases.

## Style notes

- Vanilla JS, no framework, no TypeScript. Inline styles/scripts inside the HTML files.
- Keep everything self-contained and dependency-light; the only external runtime
  dependencies are the CDN-imported Anthropic SDK and the Google/Anthropic HTTP APIs.
- Match existing formatting (2-space indent, `const`/`let`, Korean comments and UI text).
- The mute-tone palette (dusty rose `#C4817E`, sage green, background `#F8F4F0`) is
  intentional — reuse the existing CSS variables rather than introducing new colors.
