# Execution certificate: R13 native spectral decoding

Owner: protocol.md; researcher explicit frozen-forward authorization on2026-11-01.

- Profile:5090-2-spot; shphd-lite-0911; one single-node worker, resource spec n12lp.nn.i10a.2; mounted /data; actual inference restricted to device0.
- Shared runtime: existing PyTorch2.8.0+cu128 SM120 overlay; existing transformers4.53.3. Optional ABI-incompatible flash/image/audio packages disabled in process; native SDPA computation retained.
- Attempt1:pt-tcuu1t2m, submitted02:44:08UTC, FAILED before model forward at optional FlashAttention import. Source/receipt/log retained. Requested stop found already terminal; no running attempt was duplicated.
- Attempt2:pt-ev9c0mz8, submitted02:55:38UTC, status SUBMITTED/STARTING at certificate creation. Embedded three-document smoke gates all main decoding. Numerical tolerances unchanged.
- Submit path: Research_System/templates/execution/acp_submit_template.sh, dry-run and ALLOW_SUBMIT/PROTOCOL_APPROVED gates. Existing ACP compatibility wrapper uses private loopback bridge removing unsupported workspace metadata key; no credentials copied to artifacts.
- Training comparison: NOT_APPLICABLE; no optimizer, no trainable parameters, no parameter update.
- Storage: this execution directory, chunked analysis and durable logs. Scientific eligible outputs require smoke PASS and terminal_receipt.json.
- Known implementation repair: R12 arrays B are in PCA coordinates, transformed Q=V@B for raw model-unit projection. Invalid predecode setup retained under provenance/invalid_predecode_coordinate_selectors; it produced no experimental results.

Terminal runtime and actual measurements will be appended from receipts.

## Verified terminal outcome

Attempt3 pt-kz3udzv0 SUCCEEDED at2026-11-01T03:13:50.857033Z. Its first legacy-cache smoke failed and was preserved; documented A4 same-allocation resume refreshed180 unchanged-model/interface documents, then passed all smoke gates. Main15477 condition-position results completed at03:13:43.804302Z. Successful cache+decode85.2876s,peak1,387,869,184bytes,device0 only. Twelve smoke/diagnostic transformer calls plus180fresh calls =192 total; no training. Source/position/condition choices preserved. CPU final validation allPASS. Local bounded Anchor sync verified; no publication status inferred.
