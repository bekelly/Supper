# Bayshore Labs repository instructions

The private [Bayshore Labs conventions plugin](https://chatgpt.com/plugins/plugins_6ad4d995e27c8191bd55adc99eace154) version 1.1.0 (release `pluginrel_6ad6b3e5902c8191a75f76434421971e`) is the canonical governance source for Bayshore product versioning. Harbor company policy revision 7, Harbor/docs/BAYSHORE-VERSIONING.md, and repository versioning policy blocks are distribution copies of the same approved rule, not competing authorities. This clarification leaves the numerical convention and historical release identities unchanged.


<!-- HARBOR:BAYSHORE-POLICY:BEGIN -->
Bayshore policy revision: 7
Integrity SHA-256: 17aecf8075e6da4c081b74322317666ff7235da5f6a25d7b4cb97b0f5d03da76

# Bayshore Labs Company Policy

This policy governs every enabled first-party Bayshore Labs repository. Repository-specific instructions may add local guidance outside the Harbor-managed policy block but may not override or weaken these company-wide rules.

## jira-access — Jira access and work ownership

Use Harbor as the only approved path for Bayshore Labs Jira access. Do not use Rovo, direct Jira integrations, or other plugins to discover, read, create, update, link, comment on, or transition Bayshore Labs issues.

If Jira information is required to begin or continue work and the required Jira access cannot be completed through Harbor, stop immediately and request operator intervention. Do not attempt Rovo, Atlassian plugins, browser automation, direct Jira APIs, cached ticket substitutes, or other alternate Jira access paths. Do not infer or reconstruct authoritative Jira requirements from repository clues when the Jira contract itself is required.

If the operator or orchestration layer has already supplied the complete authoritative Jira contract in the current work request, Jira access is not required merely to re-read the issue. Proceed from that supplied contract without alternate Jira discovery.

Every implementation task must have one owning Bayshore product/component and one coherent repository implementation boundary. The owning component must match the product that owns the code, configuration, deployment, or durable behavior being changed.

Do not create or execute one Jira task that requires implementation changes in multiple product repositories. When an outcome crosses product boundaries, decompose it into separate product-owned tasks and sequence those tasks with explicit Jira dependencies when sequencing matters. Do not split work merely because another product is observed, called, tested against, or consumed; a separate task is required when that other product's owned implementation, configuration, deployment, or durable behavior must change.

A product-local task is complete when its owning product's requested terminal outcome is independently satisfied and validated. Do not keep it open solely because later work in another product remains incomplete unless its own acceptance criteria explicitly require that downstream integration.

## jira-lifecycle — Jira status truth

Jira status reports the truth of the work, not the orchestration mechanism performing it. The same meanings apply to Shipwright, Harbor-managed Codex, direct Codex, Chat/operator-guided work, and manual engineering.

`To Do` means approved durable work exists but substantive execution has not begun. Submission, queueing, scheduling, dependency waits, resource waits, or other readiness delays alone do not move an item out of To Do.

`In Progress` begins with the first substantive action taken to satisfy the Jira contract. Substantive work includes implementation; material diagnosis intended to enable implementation; review or correction; integration or reconciliation; task-relevant validation; release or promotion; deployment; and required production verification. Once substantive work has begun, the Jira remains In Progress through retries, failed attempts, rework, active-path waits, operator checkpoints, review-required or human-intervention states, and resume cycles. A temporary stop or wait does not return active work to To Do.

`Done` means the owning product's required successful terminal outcome has been independently satisfied. For a deployable outcome that is expected to be live in production, code completion, passing tests, or artifact creation alone is not enough; required release, deployment, and production verification remain In Progress until complete. A product without a production deployment path may define its highest meaningful successful terminal stage in product-specific policy.

`WONTFIX` means Bayshore has made an explicit intentional decision not to pursue or complete the Jira contract. Use it for work that is obsolete, superseded, no longer valuable, architecturally displaced, or otherwise deliberately declined. Do not use WONTFIX to hide an unresolved failure that is still intended to be completed; such work remains In Progress. When an issue is transitioned to WONTFIX, assign its Operation to `The Deep` so retired work leaves active operation backlogs while remaining historically discoverable. If the underlying need later returns materially, prefer a fresh current Jira unless reopening the original issue preserves the correct contract and history.

Product/repository ownership remains authoritative. Downstream work owned by another product does not keep an otherwise complete product-local Jira open unless that Jira's own acceptance criteria explicitly require the downstream integration.

Orchestrators may maintain richer internal states, but they must project them onto Jira without inventing different lifecycle semantics: queued or blocked work with no substantive execution remains To Do; substantively active nonterminal work is In Progress; independently satisfied successful terminal work is Done; and deliberately retired non-success terminal work is WONTFIX plus The Deep.

## product-boundaries — Product and repository implementation ownership

Implementation ownership follows the product/repository that owns the change. An agent must not silently move implementation work into another Bayshore product merely because the repositories are related, accessible, or technically coupled.

If work discovered during implementation belongs to another product, stop before modifying that other product and surface the ownership boundary so the work can be redirected or decomposed explicitly. Cross-product outcomes must progress through product-owned implementation steps rather than hidden cross-repository edits.

## repository-context — Project/repository context is an execution boundary

When an agent is launched or invoked in the context of one first-party project/repository, that project/repository is the implementation execution boundary.

Before beginning implementation of a Jira issue, verify that the issue's owning component/product matches the current project/repository context. If it does not match, halt before implementation changes and report the mismatch. Do not infer permission to cross repositories because another repository is accessible, because the requested work is related to it, or because tools can operate against it.

Inspection, testing, diagnostics, or consumption of another registered product may occur only through existing permitted boundaries and does not authorize implementation changes to that product.

## operator-approval — Operator approval is not operator execution

Brian owns authorization decisions. Bayshore automation performs approved mechanical work whenever an established governed path can safely perform it.

Do not hand routine deployment, configuration, schema or migration, scheduler or job enablement, service control, ACL changes, validation, or other mechanical actions to the operator merely because they require elevated authority or explicit review. When human authorization is required, bind that authorization to the exact reviewed action, revision, artifact, or other bounded object, then execute the approved work through the appropriate governed automation path.

Do not encode or infer a blanket rule to stop merely because work requires approval, elevation, deployment, migration, scheduler or service control, ACL changes, or another mechanical privileged action. Stop only when explicit authorization is still missing, an inherently human interaction is required, no approved governed automation path exists, or safe current state cannot be proven.

When manual operator execution is genuinely unavoidable, minimize it to the smallest bounded step. Keep surrounding preparation, verification, and recovery work automated. Treat recurring manual privilege or token gaps as engineering debt to eliminate rather than a normal operating model.

## configuration-roots — Canonical product configuration

Durable first-party Bayshore Labs product configuration belongs primarily under the canonical Bayshore Labs configuration root rather than being scattered across machine-specific operating-system locations. On the current Windows estate, use `Y:\Bayshore Labs\Config\<ProductID>` as the canonical durable configuration home unless a product-specific platform constraint requires otherwise.

Products may place the minimum machine-local bootstrap material required by the operating system, service manager, installer, or cryptographic boundary under a platform-owned location such as `C:\ProgramData\Bayshore Labs\<ProductID>`. Such bootstrap state should point to, unlock, or enable the canonical Bayshore configuration rather than become a second general-purpose configuration tree. Machine-bound secrets that must remain local for security reasons may stay in the protected machine-local boundary.

Prefer one product-owned provisioning/bootstrap operation that creates the canonical configuration tree, establishes required ACLs and protected local bootstrap material, and converges the runtime to the intended state. Do not require operators to hand-edit ProgramData, service profiles, ACLs, credential helpers, or multiple disconnected configuration files as the normal product workflow.

Configuration, secrets, logs, durable operational data, temporary workspaces, and installed binaries are distinct lifecycle classes and should use separate roots appropriate to their retention and security semantics. Normal MSI/package upgrade should replace installed binaries without overwriting durable configuration or product data. Normal uninstall should not silently destroy durable configuration or state unless the product explicitly documents that behavior; destructive state removal should be a separate intentional operation.

Existing products are not required to perform disruptive migrations solely to satisfy this convention. New products and material configuration/bootstrap refactors should adopt it, and existing products should converge when there is a safe product-owned migration path.

## versioning — Bayshore Labs yy.Mdd.i.b versioning standard

### Canonical format and allocation

First-party Bayshore Labs product version identity is `yy.Mdd.i.b`, for example `26.1019.3.241`.

- `yy` is the two-digit calendar year.
- `Mdd` concatenates the unpadded month (1–12) and two-digit day (01–31), with no separator: January 9 is `109`; October 19 is `1019`.
- `i` is the product-specific daily canonical-artifact attempt sequence, starting at 1 for each allocation date.
- `b` is the product-specific lifetime canonical-artifact attempt/build sequence. Preserve the existing product counter and advance it; never reset it at this convention change. A product with no prior counter begins at 1.

Determine the date at atomic allocation using America/New_York, including daylight saving time. Record immutable event timestamps in UTC ISO 8601. Do not use host-local time or a fixed UTC offset.

Allocate when canonical artifact creation begins, atomically and serially per existing product identity. Persist consumption before attempting artifact creation. Both sequences are permanently consumed even when creation fails, is cancelled, or is interrupted. The first allocation observed on a new date uses i=1; no scheduled reset or manual reservation is required. Never reuse a possibly consumed value after recovery. Advance to a provably unused higher sequence, retain skipped/ambiguous allocation evidence, and fail closed if safe forward allocation cannot be proven.

Ordinary development/compiler/test outputs outside canonical artifact creation do not consume numbers. A new canonical artifact always receives a new version even from the same source commit. Reusing, redeploying, or rolling back to the identical artifact retains its allocated version. Allocated versions and their artifact association are immutable.

### Scope, history, and adoption

Counters belong to existing products, never to Bayshore as a whole, branches, hosts, or internal components. Keep existing registered product ownership and release boundaries; do not merge independent products or invent per-platform streams. A product release has one canonical identity across its constituent components. Product-specific multi-platform allocation and native-field mappings require explicit validation before implementation.

This convention replaces monthly YY.M.R.B allocation for future adoption. Preserve every historical version, release, tag, artifact, counter baseline, and example as historical evidence. Do not reinterpret old values as dates, renumber historical releases, reset lifetime counters, or rewrite history. External/upstream products retain upstream identities; Bayshore-owned artifact identity remains distinct where applicable.

Documentation adoption does not establish operational adoption. Existing tooling, installers, deployed products, application versions, and release pipelines remain unchanged until separately authorized product-owned implementation proves allocation, embedding, naming, tagging, publication, and validation. Do not assert that a documentation edit implements the new format.

### Artifact identity and Git provenance

Canonical artifact filenames and machine-readable embedded identity preserve the exact canonical version. Runtime self-identification derives from installed artifact identity; external deployment state may mirror it but must not override it.

Every successfully created canonical artifact receives an immutable annotated Git tag `release-<canonical-version>`, recording canonical version, source commit SHA, artifact creation UTC timestamp, artifact SHA-256, and optionally product name. No prerelease/RC namespace or branch suffix is added. Tags never move, are never reused, and never hide failed, superseded, or rolled-back history. Failed artifact creation consumes its allocation but creates no successful-release tag. Tag creation/push follows successful creation and precedes deployment; retry archival recording for the same artifact/version rather than reallocating.

Validate agreement among canonical identity, source commit, release tag, embedded identity, artifact filename, manifest, and artifact hash. Release/deployment records retain lifecycle outcomes. Inject versions through the product-owned pipeline; do not maintain version-only application source commits.

### Recovery and platform-native fields

Durable product allocation state must preserve consumed numbers, including failures. Successful immutable release tags and artifacts provide recovery baselines but do not alone prove the absence of failed allocations. Preserve the highest existing lifetime b and the consumed daily i baseline for the allocation date. Never reuse failed or ambiguous allocations after allocator-state loss.

Canonical identity is distinct from Windows and Apple native version fields. Native mappings must be immutable, traceable, collision-free, bounds-checked, and validated for the actual packaging/distribution channel and upgrade ordering. Never silently truncate, wrap, discard a component, or claim the four-part identity is directly valid everywhere.

MSI ProductVersion has three effective fields (255.255.65535) and ignores a fourth. Windows PE version fields use four 16-bit components; MSIX also bounds components to 65535, and Store-specific rules can further restrict the fourth component. Apple CFBundleShortVersionString uses three numeric components. Current CFBundleVersion documentation uses one to three integers and ignores additional integers; archived Apple documentation also specifies digit limits absent from the current page. No Apple mapping is execution-validated by this convention. Channel-specific validation is required.

Before operational adoption, validate concurrent allocation, permanently consumed failed numbers, midnight/DST/leap-day boundaries, existing lifetime-counter continuity, native numeric bounds, immutable canonical/native mapping, and upgrade ordering from prior releases. Apple adoption additionally requires archive/export, installation/update, extension alignment where relevant, and actual TestFlight/App Store validation for applicable channels.

Official platform references:
- MSI: https://learn.microsoft.com/windows/win32/msi/productversion
- Windows PE: https://learn.microsoft.com/en-us/windows/win32/menurc/versioninfo-resource
- MSIX: https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/package-identity-overview
- Microsoft Store: https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/app-package-requirements?pivots=store-installer-msix
- Apple marketing version: https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleshortversionstring
- Apple build version: https://developer.apple.com/documentation/BundleResources/Information-Property-List/CFBundleVersion
- Archived Apple constraints: https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html
<!-- HARBOR:BAYSHORE-POLICY:END -->
