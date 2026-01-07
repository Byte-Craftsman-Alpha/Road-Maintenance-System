# Contributing

Thanks for your interest in contributing!

## Ground Rules

- Be respectful and constructive (see `CODE_OF_CONDUCT.md`).
- Keep changes focused and easy to review.
- Avoid introducing new dependencies unless necessary.

## What you can help with

- UI/UX improvements (Tailwind-first pages, accessibility, dark-mode correctness)
- Bug fixes
- Translation coverage / i18n improvements
- Tests and quality improvements
- Documentation

## Getting started (local dev)

1. Fork the repo and create a branch

- Branch naming suggestion: `feat/<short-name>` or `fix/<short-name>`

2. Install dependencies

- Create/activate a virtual environment
- `pip install -r requirements.txt`

3. Configure environment

- Copy `.env.example` to `.env` and fill required variables

4. Run the app

- `python app.py`

## Pull Request guidelines

- Describe the problem and the solution.
- Include screenshots for UI changes.
- Make sure the app boots and the changed pages load.
- Prefer Tailwind utilities / existing `minimal-*` components.

## Reporting issues

- Use clear reproduction steps.
- Include your OS, Python version, and any relevant logs.
