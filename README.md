# AI Personal Assistant

## Introduction

This cohort project explores how to build an AI assistant for email and calendar work. The assistant will eventually connect to an email provider, receive new-message events, understand what needs attention, and help the user take appropriate actions.

We will build the project incrementally. The first week focuses on understanding the goal and preparing a reliable development environment. Later weeks will introduce Nylas integration, email workflows, AI decision-making, persistence, and deployment.

## Why Nylas?

[Nylas](https://www.nylas.com/) gives applications one API for supported email and calendar providers. It handles provider authentication and can notify our application when something changes.

We will use Nylas in Week 2. No email account connection or webhook implementation is required in Week 1.

## Project Direction

```text
Email and calendar provider
        ↓
      Nylas
        ↓
AI personal assistant
        ↓
User reviews or approves an action
```

The final assistant should be able to:

- connect to a supported email and calendar provider
- receive and understand new email events
- classify requests and route them to the correct workflow
- suggest or perform approved email and calendar actions
- keep credentials and personal data secure

## Before Week 1

Create the accounts needed for the cohort:

1. Create a [GitHub account](https://github.com/) if you do not already have one.
2. Install Git and Python 3.12 or newer.
3. Install [uv](https://docs.astral.sh/uv/).
4. Choose an editor such as VS Code or Cursor.

## Start with Week 1

The [`week-1`](https://github.com/lindseypeng/ai-personal-assistant/tree/week-1) branch contains the complete setup guide. It covers local tools, creating your own repository, and optional Nylas preparation for Week 2.

Never commit API keys, access tokens, webhook secrets, or personal email content.
