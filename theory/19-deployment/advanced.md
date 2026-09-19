# 19 — Deployment — Advanced / Senior

**Concepts**: AWS Bedrock integration (using managed model hosting instead of self-hosting), Azure OpenAI Service integration, choosing between self-hosted k8s+vLLM vs managed cloud AI services (cost/ops tradeoff, connects back to Topic 15), CI/CD pipeline for an AI service (including eval gating from Topic 16), secrets management for multi-provider API keys at scale, blue-green or canary deployment for prompt/model changes.

**Resources**:
- [AWS Bedrock — docs](https://docs.aws.amazon.com/bedrock/)
- [Azure OpenAI Service — docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

**Code** (`code/19-deployment/03-advanced/`):
- `bedrock_provider_adapter.py` — add AWS Bedrock as another provider in the Topic 01/05 provider abstraction
- `ci_cd_pipeline.yml` — full pipeline: test → eval-gate (Topic 16) → build → canary deploy

**Interview questions**:
- Your company wants to migrate from direct Anthropic API calls to AWS Bedrock for compliance reasons. What changes, and what stays the same in your architecture? (If you built a proper provider abstraction from Topic 01/05, only the adapter changes — this is exactly why that abstraction mattered; also discuss latency/feature-parity differences to validate.)
