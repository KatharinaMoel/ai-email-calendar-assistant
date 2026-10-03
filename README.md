# Week 1: Project Setup

## This Week's Goals

1. Understand what we are building and why
2. Set up the tools used throughout the cohort
3. Create a local Python environment with `uv`
4. Create your own GitHub repository
5. Learn how `.env.example` protects secrets
6. Prepare a Nylas developer account for Week 2

Week 1 stops at project preparation. We will not build FastAPI, connect an email account, or create webhooks yet.

## The Project

Over the cohort, we will build an AI personal assistant for email and calendar work. Nylas will connect the application to supported providers. Later workflows will interpret incoming messages and help the user decide what to do next.

```text
Email and calendar provider
        ↓
      Nylas
        ↓
AI personal assistant
        ↓
User reviews or approves an action
```

## 1. Prerequisites

- Python 3.12 or newer
- Git
- A GitHub account
- [uv](https://docs.astral.sh/uv/)
- VS Code, Cursor, or another code editor

Confirm the command-line tools are available:

```bash
python3 --version
git --version
uv --version
```

## 2. Get the Week 1 Materials

Clone the cohort repository and switch to the Week 1 branch:

```bash
git clone https://github.com/lindseypeng/ai-personal-assistant.git
cd ai-personal-assistant
git switch week-1
```

## 3. Set Up the Python Environment

Create the virtual environment and synchronize the project:

```bash
uv venv
source .venv/bin/activate
uv sync
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

There is no application to run yet. This step confirms that Python and `uv` work before we start coding in Week 2.

## 4. Create Your Own GitHub Repository

1. Open [GitHub](https://github.com/) and select **New repository**.
2. Name it `ai-personal-assistant`.
3. Choose public or private visibility.
4. Do not initialize it with a README, license, or `.gitignore`.
5. Follow GitHub's instructions to connect your local project and push it.

For example:

```bash
git remote rename origin cohort
git remote add origin https://github.com/YOUR-USERNAME/ai-personal-assistant.git
git push -u origin main
git push -u origin week-1
```

Keeping the cohort repository as `cohort` makes it possible to fetch future teaching branches without replacing your own `origin`.

## 5. Understand `.env.example`

The repository includes `.env.example` to document settings that later weeks will require. It contains names and placeholders only.

When configuration begins, create a local copy:

```bash
cp .env.example .env
```

The `.env` file belongs only on your computer and is excluded by `.gitignore`. Never commit real API keys, access tokens, webhook secrets, or personal email content.

## Homework: Prepare Nylas for Week 2

The goal is account preparation only. Do not connect your inbox or configure a webhook yet.

1. Create a free [Nylas developer account](https://dashboard-v3.nylas.com/register).
2. Sign in to the Nylas Dashboard.
3. Create an application for the cohort project.
4. Note whether the application uses the US or EU API region.
5. Locate the application's client ID and API key, but do not paste or share them in class.
6. Read the [Nylas v3 getting-started documentation](https://developer.nylas.com/docs/v3/getting-started/).

In Week 2, we will add the application code, configure hosted authentication, connect a development email account, and then introduce webhooks with the necessary context.

## Week 1 Checklist

- Git, Python, and `uv` are installed
- The repository is available locally
- The virtual environment can be created successfully
- Your own GitHub repository exists and contains both branches
- You understand the purpose of `.env.example`
- Your Nylas developer application is ready for Week 2
