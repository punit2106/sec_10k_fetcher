# AI Prompt Log

Tool: Claude (Anthropic)

Approach:
Used as a pair-programming and research assistant.
AI was used to discuss implementation options, troubleshoot issues,
and generate example code. All code was reviewed, tested, and
modified manually before inclusion in the final solution.

## Key decisions made during the process

1. PDF conversion approach
   - Evaluated WeasyPrint and Playwright.
   - Chose Playwright after testing because it handled SEC filing
     layouts and tables more reliably.

2. SEC bot detection
   - Initial implementation triggered SEC automated tool warnings.
   - Identified during testing.
   - Final approach downloads filing content using requests and
     renders locally for PDF generation.

3. Browser reuse
   - Questioned whether launching Chromium per company was efficient.
   - Refactored to reuse a single browser instance.
   - Discussed production alternatives such as queues and
     dedicated PDF services.

4. Code quality
   - Iterated on logging, configuration management,
     and project structure after achieving a working solution.

## What AI helped with

- SEC EDGAR API specifics (CIKs, endpoints, filing URLs)
- Playwright usage patterns
- Debugging ideas for SEC bot detection issues
- Example implementations and code scaffolding

## What I decided

- Playwright over WeasyPrint
- Modular project structure
- Download-then-render approach
- Reuse a single browser instance
- Logging and configuration strategy