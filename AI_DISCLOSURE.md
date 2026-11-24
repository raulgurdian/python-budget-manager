# AI disclosure

I used AI tools as a tutor and reviewer while building this project.

**OpenAI ChatGPT** walked me through the coding process step by step during an interactive Python tutoring session. It explained the concepts, suggested the layered structure (CLI / service / storage / validation), and set up the exercises as outlines: function definitions, docstrings, and the prints and prompts around them. I wrote the code that fills in those parts, including the function bodies that do the validation, calculations, and file handling. When I made mistakes, it pointed out the errors and explained how to correct them. It also helped me prepare the tests, the sample data, and the documentation.

**Anthropic Claude** checked and reviewed my original code on GitHub against the assignment slides. Following that review, it made a few small fixes: Python 3.9 compatibility (`from __future__ import annotations`), a confirmation before saving an empty list over an existing file, and a clearer "file not found" message.

**What I did myself:** I wrote the function bodies, chose the data rules (allowed categories, EUR/USD only, IDs like `T001`), ran the program and the tests, and checked that invalid input is rejected with clear messages. I understand each module and can explain how it works.

**Why I used AI:** to learn how a small Python project is split into testable layers, with guidance at each step, while still writing and understanding the code myself.
