# Phase 1 Discussion Log

**Phase:** 01-network-restructuring
**Date:** 2026-08-28
**Mode:** default

## Discussion

### Gray Areas Identified
1. Confirm exact removal scope
2. Comment cleanup for removed lines
3. IPv6 preservation confirmation
4. Section header update

### User Selections
- **Selected:** Confirm exact removal scope (remove only 3 FSOS registry values, keep everything else)
- **Not selected (open to Claude's discretion):** Comment cleanup, IPv6 preservation, Section header update

### Decisions Made
1. Remove exactly 3 FSOS `!registryValue` directives from Section 29 (MaxUserPort, DisableBandwidthThrottling, FastSendDatagramThreshold)
2. Remove inline `# (FSOS)` comments along with the directives
3. Keep IPv6 preserved (per existing section header)
4. Update Section 29 header comment to reflect "Vain-only"

### Deferred Ideas
- Modularizing custom.yml — Phase 3
- Full verified feature matrix — Phase 2
- Bug verification — Phase 4

---

*Phase: 01-network-restructuring*
*Discussion completed: 2026-08-28*
