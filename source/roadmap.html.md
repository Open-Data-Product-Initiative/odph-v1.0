---
title: Roadmap | ODPH v0.2
---

# Roadmap

| Phase | Direction |
| --- | --- |
| v0.2 Phase 1 | Guided, object-level workflows using one `KentaroAction` and one validated specification file per Maysano resource write. |
| v0.2 Phase 2 | Validated `KentaroChangeTask` orchestration that still executes through individual Maysano API calls. |
| v0.3 | Planned MCP interface to Kentaro capabilities: `kentaro.create_change_task`, `kentaro.validate_change_task`, `kentaro.submit_change_task`, and `kentaro.get_change_task_status`. MCP does not replace Maysano APIs or become the record store. |
| Future | Maysano-native composite execution may add server-side validation, locking, atomic execution, and grouped audit. This is not required for v0.2. |
