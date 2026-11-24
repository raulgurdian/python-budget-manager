# AI disclosure

I built this project with substantial help from AI tools, and I want to be clear about which parts.

**OpenAI ChatGPT** (during an interactive Python tutoring session) explained Python concepts, suggested the layered structure (CLI / service / storage / validation), and drafted most of the code, the unit tests, the sample data, and the documentation.

**Anthropic Claude** reviewed the finished repository against the assignment slides and made small fixes: Python 3.9 compatibility (`from __future__ import annotations`), a confirmation prompt before saving an empty list over an existing file, a clearer "file not found" message, and this disclosure's wording.

**What I did myself:** I chose the requirements and data rules (allowed categories, EUR/USD only, IDs like `T001`), ran the program and the tests, checked that invalid input is rejected with clear messages, and reviewed the code so I can explain each module.

**Why I used AI:** to learn how a small Python project is split into testable layers and to get a working, validated Release 1 within the practice time. I treated the AI output as a draft that I had to run, test, and understand, not as finished work.
