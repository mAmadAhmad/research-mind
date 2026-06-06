# ResearchMind — Agentic Research Assistant

## Problem
When researching new topics, product ideas, or staying current 
with a field, existing LLM tools give confident answers with 
no verifiable sourcing. You cannot trust what you cannot verify.
Manual research across Reddit, papers, and news is time-consuming
and inconsistent.

## Solution
An agentic research assistant that:
- Accepts a research query or topic
- Searches real sources (web, Reddit, Wikipedia, ArXiv)
- Returns a structured, sourced summary saved to a knowledge base
- Shows exactly where every claim came from

## What It Does NOT Do
- It does not generate answers from model memory
- It does not manage resumes or documents (separate concern)
- It does not replace deep reading — it surfaces what to read

## Core User Flow
1. User inputs: topic + research goal + sources to check
2. Agent searches each source via MCP tools
3. Agent synthesizes findings with citations
4. Output saved to local knowledge base as markdown
5. User can query saved knowledge base later

## Tech Stack
- Agent brain: Claude via Anthropic API / OpenAI API
- Tool protocol: MCP (one server per source)
- Backend: FastAPI
- Storage: Local markdown files → later vector DB for RAG
- Evals: Relevance + coverage scoring per query

## MCP Servers (Scope)
- search_server: web search tool
- wikipedia_server: article search + fetch
- reddit_server: subreddit search via Reddit API
- arxiv_server: paper search (AI/ML topics)
- knowledge_base_server: read/write local research files

## Out of Scope (v1)
- Google Drive integration
- Real-time alerts or email digests
- Frontend UI (CLI first)

## Success Criteria
- Given a topic, returns 5+ sourced findings in under 60 seconds
- Every claim links to a real URL
- Results saved and retrievable by topic
- Evals show >80% relevance on test queries
