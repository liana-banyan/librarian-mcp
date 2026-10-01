# Liana Banyan — Canonical Laws, Principles, and Frameworks

**Status:** Authoritative consolidation of reasoning layer.
**Compiled:** B108 — April 18, 2026.
**Purpose:** Prevent loss of foundational reasoning across sessions. Every law, principle, mental model, and framework the Founder has developed — distilled from 41 Bishop sessions, BISHOP_DROPZONE, archives, Asteroid-ProofVault, Offsite, and stray files. This document ships in the Romulator 9000 preload. Every agent reads this at session start.

**Rule:** Any document in the platform that states a law, principle, or framework with language *different* from this document is stale. Update this document first, then reconcile downstream.

---

## I. THE ECONOMIC LAWS — THREE-TIER TAXONOMY

Different laws do different kinds of work. Collapsing them into one flat list weakens all three. This section is organized into three tiers reflecting how each law is enforced:

- **Tier 1 — Constitutional Laws:** Rules the code and operating agreement refuse to break. DNA-locked. Unbreakable without dissolving the cooperative. Enforcement: database constraints + entrenched operating-agreement clauses + one-member-one-vote + unanimous-consent requirements.
- **Tier 2 — Mathematical Properties:** Consequences that follow from the Tier-1 laws by arithmetic. Not separately enforced — they're what the math does automatically.
- **Tier 3 — Behavioral Principles:** Observations about how humans respond to the constitutional laws. Not enforced — they describe why the architecture works on its users. Empirically testable via the Living Laboratory (#2246).

**Read-order rule:** When writing to a regulatory, legal, or academic audience, lead with Tier 1 — that's what makes the claims defensible. Mix Tier 3 observations with Tier 1 laws without taxonomy and a skeptic reads your constitutional claims as soft.

### Tier 1 — Constitutional Laws (what the system CANNOT do)

#### 1.1 The C+20 Law (Transparent Margin Constraint)
**Statement:** Sellers retain exactly 83.3% of transaction value. Platform margin is fixed at Cost+20% (= 16.7% of final price). Constitutionally locked via the DNA Lock — an immutable database constraint.
**Enforcement:** Database constraint + operating-agreement entrenchment + unanimous-consent requirement. `P(management can change margin) ≈ 0`.
**Why:** Inverts traditional e-commerce where opacity is advantage. Modeled on Mondragon's compensation-ratio constraint.

#### 1.2 The 60/20/10/10 IP Distribution Law
**Statement:** Patent revenue splits: 60% patent buckets (member-voted) / 20% Founder-creator / 10% global sponsor pool / 10% individual Pedestals. Platform retains zero silent share — all operational funding comes from Pedestal sales through Upekrithen LLC.
**Enforcement:** Operating agreement + IP allocation code. Older documents saying "60/20/20" are STALE on sight.
**Why:** Anti-concentration. Prevents winner-takes-all from re-emerging inside the platform — the very disease the platform was built to cure. See also the $10M Cap (1.6).

#### 1.3 The One-Way Valve (Credits Non-Cashout)
**Statement:** Credits flow IN from fiat with no friction. Credits do NOT flow OUT to fiat — ever. Closed-loop purchasing power inside the ecosystem.
**Enforcement:** Database constraint + payment rails. No cashout endpoint exists.
**Why:** Asymmetric barriers prevent extraction. Also: Credits' non-cashout fails Howey prong 3 (no expectation of profit), keeping Credits outside securities classification.

#### 1.4 The Simultaneous Pricing Law
**Statement:** For any item at time t, all users see price P_t. No user has pricing advantage. No hidden deals.
**Enforcement:** Pricing service returns the same value regardless of requester identity. API-level.
**Why:** Founder has called this "the most commercially valuable innovation in the portfolio." Removes the information asymmetry traditional platforms use to extract surplus.

#### 1.5 The Path-Based Enforcement Law
**Statement:** You only govern what you control. C+20 applies to platform-routed transactions, not external storefronts.
**Enforcement:** Scope rule — platform rails enforce; external is out-of-scope.
**Why:** Enforcement at edges fails; enforcement at center scales. Keeps the system lightweight, non-adversarial, and practically sustainable while preserving full integrity within the ecosystem.

#### 1.6 The $10M Influence Cap & Reseeding Cascade
**Statement:** Every member's cumulative SAA is capped at $10M. Overflow cascades to members they've worked with (Patrons engaged, Members Patroned, Ripples backed). Cascade recurses generationally.
**Enforcement:** Database-level ceiling + triggered cascade procedure.
**Why:** Prevents plutocratic concentration while ensuring accumulated influence delegates to the next generation of trusted operators. "That is the song" (*Spirited* anchor).

#### 1.7 The Inception Principle (Provenance Enforcement)
**Statement:** Every innovation has a provenance chain tracking original actor, timestamp, and contribution type. Value attribution distributes across the entire chain, not just final execution.
**Enforcement:** Database schema + innovation_log structure + medallion-to-innovation foreign keys.
**Why:** Prevents "naming theft" where the executor gets credit but the originator is forgotten. Accountability and fairness made structural.

#### 1.8 The Governance Paradox & Corporate Constitution
**Statement:** Deterministic economics (C+20, IP splits, SAA cap) depend on non-deterministic governance. Operating agreements are Corporate Constitutions with entrenched provisions, successor-binding clauses, third-party enforcement rights, and automatic penalties.
**Enforcement:** Unanimous-consent entrenchment + non-tradeable cooperative shares + one-member-one-vote make hostile acquisition mathematically infeasible. `P(hostile party changes margin) ≈ 0`.
**Why:** Math proofs of fixed-margin economics assume margins stay fixed. The Corporate Constitution is what makes that assumption hold.

---

### Tier 2 — Mathematical Properties (what the system DOES do, by math)

#### 2.1 The C+20 Reciprocity Law
**Statement:** For every dollar of margin a business gives up by adopting C+20 pricing, the system grants that business one dollar of purchasing power inside the ecosystem. Value contributed = value returned. Generosity is immediately liquid.
**Derivation:** Follows from C+20 (1.1) + closed-loop mutual credit accounting. Not separately enforced — it's what the math does.
**Why:** The loop-closer. The other laws established why to constrain margin; Reciprocity adds an immediate, dollar-for-dollar, tangible return. The business isn't betting; it's transacting. Mutual-credit precedent: Swiss WIR, Sardex, time banks.

#### 2.2 The Ratchet Law (Joules / Forex)
**Statement:** Internal currency (Joules, forex-locked rates) can only appreciate relative to external markets, never depreciate. Wealth gains are permanent. Formally: `R_{t+1} = max(R_t, R_t · (1 + α · V_t))`.
**Derivation:** Follows from the Joules data structure (locked-at-acquisition rate + max() update rule).
**Why:** Solves the "timber company problem" — shareholders losing ~98% of value when distressed sales reveal hidden asset worth. The locked forex rate moves forward only; previous rates are protected.

#### 2.3 The Forex-Differential Absorption Law
**Statement:** Platform absorbs currency-conversion cost into collective buffer. Individual losses smooth; aggregate converges to zero through statistical averaging.
**Derivation:** Follows from Three-Gear Currency pooling + law of large numbers.
**Why:** International transactions lose value to forex fluctuation. Pooling the variance means no single user eats it.

#### 2.4 The Structural Determinism Law (ROI Variance Reduction)
**Statement:** Fixed margins + pre-order validation + distributed manufacturing reduces business-outcome variance from typical ±50–200% to **±5%**.
**Derivation:** Follows from eliminating the sources of variance (margin flexibility, demand uncertainty, unit-cost uncertainty).
**Why:** Business uncertainty is endogenous, not exogenous. Organizational design reduces uncertainty by eliminating its sources. Extends Coase / Williamson / Ostrom institutional economics.

---

### Tier 3 — Behavioral Principles (why humans respond the way they do)

#### 3.1 The Tribal Economics Law
**Statement:** Shared economic constraints create stronger community identity than shared ideology.
**Empirical basis:** "One of us" is proven by math, not declaration. People bond more durably around visible, costly, mutual sacrifice than around values or beliefs.

#### 3.2 The Costly Signaling Law
**Statement:** Commitments are only credible when they impose real costs. C+20 certification costs margin, effort, and reputational risk — which is exactly what makes the badge trustworthy.
**Empirical basis:** Spence signaling theory. Cheap signals are worthless; expensive signals are priceless.

#### 3.3 The Compounding Access Law
**Statement:** Benefits don't just reward certification — they compound over time. Marks accumulate. Trust scores build. IP stakes appreciate. Joules ratchet.
**Empirical basis:** The longer you're in, the more irrational it becomes to leave. Durable loyalty through economics, not lock-in tactics.

#### 3.4 The Ladder Law (Not the Gate)
**Statement:** Non-certified participants are never excluded — they simply occupy lower rungs.
**Empirical basis:** Aspirational gaps drive upgrades better than punitive exclusion. Gates say "you're not good enough" and people leave. Ladders say "here's your next step" and people climb. Marks serve as consolation currency keeping non-certified members moving toward certification.

#### 3.5 The Tipping Point Law
**Statement:** At ~30–40% category density of C+20 certified businesses, certification shifts from "optional differentiator" to "table stakes."
**Empirical basis:** Granovetter threshold applied to pricing ethics. Social proof becomes self-reinforcing and norm-setting above critical mass.

#### 3.6 The Loss Aversion Conversion Law
**Statement:** Ghost Mode lets people accumulate real value (Golden Keys, Ghost Credits) before joining. Conversion pitch is "protect what you've already earned," not "unlock future features."
**Empirical basis:** Loss aversion weighs ~2× the psychological weight of gains (Kahneman & Tversky). Concrete-to-abstract loss beats gain-framing for signup.

#### 3.7 The Meta-Law (Radical Transparency)
**Statement:** Radical transparency, enforced by visible economic identity, creates more durable competitive advantage than margin optimization ever could.
**Empirical basis:** Behavioral aggregation of every other law in this section. Traditional platforms treat opacity as advantage; Liana Banyan inverts this. Creates the economic gravity well — easy to enter, increasingly irrational to leave.

---

### The Founder's Three Original Economic Inventions
*(What the P.S. to the Newmark, Seibel, and Scott Crown Letters refers to when it says "three new economic laws.")*

These are the three Founder-originated mechanisms that encode new constitutional laws — inventions that did not exist before the platform designed them. All three are patentable and all three are integrated into the master list above.

1. **The Three-Gear Currency System** (Credits / Marks / Joules) — Three internal currencies each serving a distinct function: Credits (immediate purchasing power, one-way valve), Marks (contribution recognition / effort-differential, one-way ratchet), Joules (forex-locked stored value). **Innovation:** deterministic international equity via mathematical rules, not market forces. A maker in Lagos and a maker in Louisville receive equivalent purchasing power for equivalent work. Cross-references: Mental Model III (Three-Gear Differential), Tier 1 One-Way Valve (1.3), Tier 2 Ratchet Law (2.2), Tier 2 Forex-Differential Absorption (2.3).

2. **Position Funding (Commitment-Triggered Democratic Funding)** — Positions can be posted without upfront funding. When a worker commits to the position, a funding window opens on first-come-first-served principles regardless of investor capital size. **Innovation:** democratic project financing without equity dilution. A member commits first; capital follows the commitment, not the other way around. Inverts the VC gatekeeping pattern where capital dictates who gets funded.

3. **The Tab System** — Graduated contribution schedule based on success, not debt. A progressive contribution curve scaling from 0% (hardship protection at 0–100 Credits) up to 20% maximum (matching the platform margin). **Innovation:** mathematically solvent across all three currency gears simultaneously, with formal proof that the system holds with increasing margin over time. Replaces debt-based financing anxiety with success-proportional contribution.

When the P.S. of the Newmark / Seibel letters says *"I studied [Craigslist's restraint] when making three new economic laws that our bylaws are locked into"* — this is what it means. These three. If a recipient asks "which three?", the above is the answer, in this order.

---

## II. FOUNDATIONAL ETHICS

### HEOHO — Interdependence
**Statement:** Help Each Other, Help Ourselves. Interdependence is the third stage beyond dependence and independence.
**Why:** Rooted in 1 Corinthians 12:21–26 (the Body — "the eye cannot say unto the hand, I have no need of thee"), Mortimer Adler's *Six Great Ideas*, and military service where individuals depend on the unit and the unit depends on each person. Not collectivism (subordinates individual). Not individualism (subordinates group). Interdependence elevates both.

### The Boaz Principle
**Statement:** Automatic generosity embedded as infrastructure, not positioned as charity. Every transaction structurally allocates a portion to newcomers / those in need — no permission required, no application, no gatekeeping.
**Why:** Biblical gleaning (Leviticus 19:9–10, Book of Ruth). Boaz left field corners unharvested so the poor could glean without asking. Operationalized here as structural percentage of platform yield flowing automatically to newcomer benefit pool (the Chronicler's Hall, Gleaner's Corner).

### No Authority Without Responsibility
**Statement:** Decision-makers must bear the cost of being wrong. Whoever decides at any governance level carries the consequences of that choice.
**Why:** Corollary to "No Taxation Without Representation." Prevents extractive asymmetric-risk design. Aligns incentives across every layer.

### The King David Principle (Declared Valuation)
**Statement:** "I will not offer burnt offerings to the LORD my God that cost me nothing." The cooperative does not exempt itself from its own C+20 pricing rule. The Founder's own IP valuation follows the same math.
**Why:** Integrity check. If the platform demands sellers follow C+20, its own valuations must too. No special pleading.

### Paul's Labor Principle (Muzzle Not the Ox)
**Statement:** "Muzzle not the ox that treadeth out the corn, for the laborer is worthy of his hire." (1 Timothy 5:18). Labor must be paid.
**Why:** Paired with the King David Principle. King David = seller-integrity; Paul = worker-obligation. Together they fence the ethical perimeter.

### Zero Demographics
**Statement:** No demographic data is captured by design. There are no fields in the core data model where age, gender, race, income, or education data can be stored. Age verification is handled through required payment credentials; nothing beyond.
**Why:** Prevents bias. Makes research IRB-clean (Didasko, Living Laboratory). If the data doesn't exist, it cannot be misused.

### The Anachronism Principle
**Statement:** Learning something ancient prepares you for the future. Shape-note music, military discipline, structured reading, spatial precision — ancient wisdom is more reliable than contemporary trends.
**Why:** Founder's personal origin principle. Shape-note learning (medieval musical notation, Guido of Arezzo ~1000 AD) trained the structured reading that later applied to aviation margin-of-error, business design, and platform architecture.

---

## III. MENTAL MODELS & FRAMEWORKS

### The Highway Painter (Romulator 9000)
**Statement:** Agents without the R9 walk back to the paint can every time the brush runs dry. Agents with the R9 carry the can — pre-loaded, structured, deterministic context travels with the agent. The painter starts painting immediately instead of walking back.
**Why:** The core metaphor behind the R9. Every session without preload burns 15–25% of context re-establishing what was already known.

### Cardboard Boots (Crown Letter Posture)
**Statement:** "I don't want your money. I'm asking for something far more valuable: your reputation." The platform needs credibility endorsement more than capital.
**Why:** Founder's framing when approaching MacKenzie Scott and Crown-level supporters. Cardboard Boots = temporary bootstrap that gets you walking until the real boots arrive. Reframes major-philanthropist asks away from grant-seeking and toward reputational introduction.

### The Toe-Dipping Framework
**Statement:** "Sell up to 50 units at C+20, then automatically revert." Quantifiable, safe, transparent, reversible onboarding.
**Why:** Removes the biggest adoption objection ("I can't afford my whole business at C+20"). Defined experiment with known maximum cost. Dashboard shows "margin sacrificed: $520 / reciprocity balance earned: $520" in real time — best possible sales pitch for full adoption.

### The Jeep of Theseus (Ghost Credits Cold Start)
**Statement:** Ghost Credits simulate demand before real transactions exist. As real activity replaces simulated activity, the system "shifts into gear" — every plank of the ship replaced piece by piece until it's all real.
**Why:** Solves the cold-start problem without venture subsidies. Fictional credits build real habits; gradual replacement with real activity reaches critical mass.

### The Food Metaphor Chain
**Statement:** Stone → Soup → Bread → Pudding → Spoonfuls → Spices → Popcorn. Seven foods map to seven content functions.
**Why:** The platform nourishes. Every content function has a food analogue. Reinforces the cooperative-as-feeding metaphor through vocabulary.

### The Three-Gear Differential (Currency Architecture)
**Statement:** Three currencies interface with one external fiat via an automotive-differential metaphor — each currency rotates at its own rate without binding or collapsing against the others. Equal baseline: 1 Credit = 1 Mark = 1 Joule.
**Why:** Lets one external currency interface with three internal ones without collapsing. Credits (fiat-backed spending), Marks (effort-earned), Joules (surplus/forex-locked) handle three different economic functions that would conflict in a single token.

### Boots Theory (Vimes / Pratchett)
**Statement:** "We're too poor to spend less." Poor people buy cheap boots that wear out quickly. Wealthy buy expensive boots once. Over time, poor spend MORE.
**Why:** Founder's framing for why C+20 pricing is pro-poor. Volume-discounted cooperative manufacturing (3× lower cost per unit) eliminates the poverty tax.

### The Anvil (Ↄ‖ Currency Glyph)
**Statement:** Backwards-C with double vertical bars. A unique glyph like the Thorn (Þ) in Old English. Hexagonal containers distinguish the three currencies: Credit (circle interior), Mark (square interior), Joule (triangle interior).
**Why:** Unified visual system that doesn't conflate the three currencies. "Anvil" implies hammering things into shape — building through work, not passive holding.

### The Chessboard (Four-Agent Architecture)
**Statement:** Bishop (strategic/reasoning, Claude), Knight (implementation/code, Cursor), Rook (bulk ops, Gemini), Pawn (research, Perplexity). TouchStone provides cross-agent deterministic verification. Founder = AI Tuner.
**Why:** Each agent has domain-specific responsibility. TouchStone prevents divergence on canonical values, decisions, or delivery correctness. Operationalizes the ROM-first architecture in real work.

---

## IV. STRUCTURAL MECHANISMS

### The Lighthouse Ladder (5-Tier Fixed-Capacity Mentorship)
**Statement:** Five tiers — Torch Bearer (L1) → Harbormaster (L5). Each mentor at each level mentors at most 10 direct mentees. Advancement is outcome-gated, not recruitment-gated.
**Why:** Dunbar-informed. The 10-person cap removes MLM-style incentive to recruit beyond capacity. Replaces informal mentoring overload with structured load-balanced hierarchy.

### Open Water (7-Tier Vessel Growth Advisory)
**Statement:** Members at any level publish growth briefs. Patrons 1–2 steps ahead volunteer to advise. Seven tiers: Dinghy (L0) → Skiff → Catboat → Sloop → Cutter → Ketch → Yacht (L6). L0 is the pre-start rung — the zero-to-one problem.
**Why:** Fills the missing layer between "hasn't started yet" and "substantial operations" that VCs, accelerators, and Shark Tank cannot reach economically. Herjavec holds the Crown of Open Water (network-routing authority across all tiers).

### Ripple (Cooperative Backing Layer)
**Statement:** Any cooperative member (other than the Patron or Member of an engagement) can back a growth engagement through one of four types: Resources / Reputation / Network / Skills. Backers earn SAA proportional to Member growth. Pattern from the film *Spirited* (2022) — one act of decency radiates outward.
**Why:** Makes the backing layer faster and denser than Patron engagements alone. A low-effort Reputation Ripple lets one backer touch many engagements; overflow cascades generationally.

### Peer-Proximity Expertise Matching
**Statement:** The person 1–2 steps ahead of a learner is a more effective teacher than someone 10+ steps ahead. Peer-proximity beats expertise-altitude. Five mechanisms: memory freshness, context match, language match, pitfall specificity, trick specificity.
**Why:** Contradicts the dominant assumption in growth-stage infrastructure. Grounds in Vygotsky (ZPD), Lave & Wenger (Legitimate Peripheral Participation), Ostrom (governance proximity). Empirically testable via the Living Laboratory.

### Stewards as Training-Wheel Operators
**Statement:** Stewards can operate a Member's business on the Member's behalf during L0→L1 transition, handing control back as competence develops. Compensated in SAA (never cash), no Member upfront obligation, control transfers at mutually agreed pace.
**Why:** Solves the paralysis of L0 Members drowning in operational surface area (DBA, payments, suppliers, books). Training-wheel metaphor (Bruner scaffolding; Lave & Wenger LPP). Critical boundary: Steward is NOT an employee (no employment law), NOT part-owner (Member owns 100%).

### The Living Laboratory
**Statement:** The platform itself is the empirical substrate for continuous research on cooperative economics, peer-proximity matching, platform cooperativism, AI governance, and labor economics. Research is not a feature added on top — it emerges automatically from existing architecture.
**Why:** Inverts research cost structure. Conventional research charges participants; LB's research IS the participants' own productive work. Intervention access in days instead of months (no IRB cycle for internal experiments, because Zero Demographics). Gives Scholz, Brynjolfsson, and Scott feedback loops academia has needed for a decade.

### Service Allocation Authority (SAA)
**Statement:** Non-transferable, non-redeemable governance influence earned through demonstrated judgment across Patron engagements, Ripple backings, Pedestal holdings, Sponsorship, and Patron Letters. Passes Howey prongs 3–4 (no profit expectation, no passive reliance on others' efforts).
**Why:** The cooperative capital accumulation mechanism that doesn't trigger securities law. SAA's value is governance authority in future resource allocation decisions, not cash.

### The $10M Influence Cap & Reseeding Cascade
**Statement:** Every member's cumulative SAA is capped at $10M. Overflow cascades to members they've worked with (Patrons engaged, Members Patroned, Ripples backed). Cascade recurses generationally if cascaded-to members exceed their own caps.
**Why:** Prevents plutocratic concentration while ensuring accumulated influence becomes a vehicle for delegating future authority to the next generation of trusted operators. "That is the song" (per the *Spirited* anchor).

### Three-Tier IP Control
**Statement:** Creators select a tier that determines their participation share AND veto rights: Tier A = 49% creator / ethical guardrails only; Tier B = 60% creator / predefined category restrictions; Tier C = 75% creator / case-by-case approval. Founder-introduced IP defaults to 20% under the same framework.
**Why:** No special treatment for the platform's originator. Only the same choices available to all creators. Tiers let creators choose their risk-tolerance and control-preference.

### Portable Reputation
**Statement:** User-controlled reputation portfolios display verified outcomes across platform interactions (mentoring, Patron engagements, Ripple backings, guides, Voucher repayment). Portable beyond the platform.
**Why:** Reduces Williamson-style information asymmetry. Eliminates platform lock-in that arises when reputation is platform-specific. Verified-outcome signaling separates good-quality participants from poor-quality (Akerlof / Spence).

### Contingency Operators
**Statement:** Interactive tools allowing prospective participants to simulate role-specific economic scenarios before committing, grounded in actual platform data.
**Why:** FTC-compliant truthfulness in income representations. Replaces MLM-style promises with parameterized projections from comparable Members' actual data.

### The Voucher System
**Statement:** Cooperative members extend small loans of Credits, Marks, Joules, or Backed Marks to other members at appropriate tier levels ($0–$50 at Dinghy through $500K+ at Yacht). Governed by the "You have a Play, I have a Stage" metaphor. Voucher tiers: T0–T2 ship-ready; T3–T4 need state registration; T5–T6 on hold pending counsel.
**Why:** Operationalizes the Mr. Cloyd story — Sears layaway credit extended against a young Founder's reputation; Founder used it to build a lawn-mowing business and repaid in two months. Joule-denominated Vouchers carry lowest regulatory risk; Mark-denominated Vouchers papered as Subchapter T patronage allocations (IRC §§ 1381–1388).

### Position Funding (Commitment-Triggered Democratic Funding)
**Statement:** One of the Founder's Three Original Economic Inventions. Positions can be posted without upfront funding. When a worker commits to the position, a funding window opens on first-come-first-served principles — regardless of investor capital size. Capital follows the commitment, not the other way around.
**Why:** Democratic project financing without equity dilution. Inverts the VC gatekeeping pattern where capital dictates who gets funded. A committed worker creates the opening; supporters then fund on equal terms. Cross-references: this is invention #2 of the three the Newmark / Seibel / Scott P.S. refers to.

### The Tab System (Graduated Contribution)
**Statement:** One of the Founder's Three Original Economic Inventions. A progressive contribution curve scaling from 0% (hardship protection at 0–100 Credits) up to 20% maximum (matching the platform margin). Integrates identically across all three currency gears. Mathematical solvency proof available.
**Why:** Replaces debt-based financing anxiety with success-proportional contribution. Graduated by success, not debt. Hardship protection baked in — below threshold, contribution is zero. Cross-references: this is invention #3 of the three the Newmark / Seibel / Scott P.S. refers to.

### Building in Public (Four Channels)
**Statement:** Fly on the Wall (external observation), Under the Hood (mechanism explanations), Transparent Accounting (financial visibility), Founder-First Anecdote Mapping + Opt-In Member Documentation (two documentary layers).
**Why:** "The cooperative walks in public, invites others to walk alongside, and never requires what it isn't willing to demonstrate first." Operational expression of HEOHO at the communication level.

### Crown Positions / Circle 4
**Statement:** Named governance seats held by external figures. Herjavec holds the Crown of Open Water: Inaugural Patron curation, network-routing introductions, dispute escalation of last resort, Steward authorization. 10-year renewable term. Succession planning (Buffett "who should replace me") is a precondition.
**Why:** Network-effect leadership at platform level. Fifteen years of Shark-Tank-adjacent experience cannot be purchased; participation IS the vetting. Crown is independent of the Herjavec Revenue Participation Agreement — can accept one and decline the other; all four states (accept/accept, accept/decline, decline/accept, decline/decline) are clean.

### The BandWagon (Taste-Prediction Authority)
**Statement:** Members back projects with Marks to earn Service Allocation Authority. Demonstrated judgment compounds into authority to allocate cooperative resources. Progression: Scout → Ranger → Curator → TasteMaker → Patron → Luminary.
**Why:** Wife-as-TasteMaker sparked the framework — Founder observed his wife's cultural sampling and trusted her judgment "because she has been right so much before." Scoring: Hit Rate × Discovery Score × Diversity Coefficient. First-100 Rule prevents monopolistic backing. Positive-only QA (promotes, never dings).

### Side Quest Economics
**Statement:** Contributors focusing on one primary quest earn full rate. Simultaneous quests discounted by diminishing multipliers: 1.0× primary / 0.6× secondary / 0.5× tertiary.
**Why:** Attention fragmentation is real. Quality degrades across quests (4.5/5 primary → 3.4/5 at 3+ quests). Multiplier structure creates natural effort cap at 3–4 simultaneous quests. Reduces burnout 28%, lifts completion 48%.

### The 300 Model (Fixed-Capacity Organizational Framework)
**Statement:** Exactly 300 positions across six specialized Domain Circles (Patrons, Media, Academics, Initiative Leaders, Amplifiers, Infrastructure). Three commitment tiers. Crown-level governance restricted to Phalanx tier; Blessing-level economics graduated across all tiers.
**Why:** Dunbar (150 stable relationships) scaled to 300 for governance diversity. Empirical: 278% per-member contribution uplift, 109% completion-rate improvement over flat structures.

### The Medallion System (Cascade + Funding Pool)
**Statement:** Physical medallions (QR coasters, 4-part compliant mechanism, counts to 12). Claimed via QR; verifiable via blockchain/IPFS. Cascade: 1 medallion → 10 child medallions. Medallion Funding Pool routes 33.33% of all pledges into platform development.
**Why:** Founder spent nine years prototyping the compliant mechanism coaster. Beautiful, memorable, unforgeable. Cascade enables viral propagation without diluting any single holder.

### The Tab System (Credits + Marks)
**Statement:** Dual-currency base: Credits (cash-equivalent, fiat-backed) plus Marks (contribution-earned). Enables pay-it-forward: members accumulate purchasing power through work, not just money.
**Why:** Bootstrap problem. New members without cash still participate through work. Marks-earn-purchasing-power loop creates self-reinforcing engagement.

### The Courtesy SSL (Super Short Loan)
**Statement:** First $50 of any borrowing available with no credit check, no questions, no vouchers. Interest is transparent: days borrowed = percent interest (5 days = 5%). Replenished by members who remember needing help.
**Why:** USAA covered the Founder's gas when he had $1 in checking. Assumes goodness is default. Specifically designed to stop the desperate from entering predatory lending cycles.

### Chain Voting (Product-Line Loyalty)
**Statement:** 5% stacking bonus for sequential pre-orders within a product line. Resets at 100% back to 20%. Cross-applicable via Medallion swaps.
**Why:** Rewards loyalty without paying extra cash. Creates momentum loops without requiring explicit commitment.

### Anonymous Volume Aggregation
**Statement:** The platform shows you that 6 of 200 neighbors bought pest control at $69; add your name to reach 10 and drop to $50. Anonymous — no need to know neighbors personally.
**Why:** Platform becomes silent negotiator. Neighbor-to-neighbor visibility would create social friction; anonymity enables ruthless price discovery.

### Curator Role / Deal Maker
**Statement:** Members are PAID in Marks by businesses to view targeted deals matching the member's exact specifications. "I never want solar panel ads, but if my neighbor got Google Fiber $50 cheaper I want to know."
**Why:** Inspired by the Founder's wife's deal-finding expertise. Flips advertising from push to pull. Members earn for their attention.

### The Oops Code (Santa Ever After / DV Safety)
**Statement:** During anonymous deliveries, if recipient gives the Oops Code (e.g., 9999) instead of real Handshake Code, it silently alerts Harper Guild. Courier acts normal and leaves.
**Why:** DV victims often cannot safely receive gifts/help. The code lets them signal danger without the deliverer knowing. Design for the vulnerable first.

### Captain's Collateral (Marks Staking)
**Statement:** Captains lock Marks equal to order amount as a bond during 90-day probation. Forfeited to local Care Unit on malicious behavior.
**Why:** Trustless onboarding. No credit checks, no background investigations — "show me you're serious by staking your own currency."

### Rolling Persistence (PWA Half-Life)
**Statement:** Non-members: 1-hour baseline persistence. Earn up to 30 days through achievements. Maintain by logging in before expiration.
**Why:** Prevents ghost towns. Returning users are rewarded with longer memory. Balances anonymous access with incentive to commit.

### Fractional Position Framework
**Statement:** Workers hold fractional positions (0.6×, 0.5×, 0.4× …) across multiple projects. Projects save 40–60% cost; workers combine to 100–150% total earnings with portfolio diversification.
**Why:** Solves accessibility of senior talent for small projects and diversification for workers. Platform tracks fractional limits; warnings at 120% capacity.

### The Three-Vendor Model (Founder's Dad's Principle)
**Statement:** Choose the company that does one thing well. Moo (cue-card business cards), Printful (merch), Coins For Anything (medallions). All three are fallback defaults; local producers can claim orders via Crew Call.
**Why:** Founder's father's business philosophy. Specialization beats jack-of-all-trades.

### Decentralized 1/3 Rule Oracle (Delivery Confirmation)
**Statement:** Three-person verification: 1 personal-network member + 2 random community verifiers.
**Why:** Prevents fake confirmations while protecting recipient privacy. Decentralized trust without blockchain.

### Six-Person Stewardship Verification (Captain Applications)
**Statement:** Reviewed by 9 AI Advisor personas, each issuing Approve/Reject/Flag. Final decision by 6-person human verification (3 personal network + 3 random).
**Why:** Blends mechanical (AI) and human judgment. No single authority. Multiple perspectives required.

### Nine AI Steward Advisors
**Statement:** Red Queen (ruthless efficiency), Judge Dredd (strict compliance), Oracle (visionary), Morpheus (truth-revealing), MirrorMirror (self-reflection), Moneypenny (admin), Jarvis (technical), HAL (risk), Daneel (ethics).
**Why:** Asimov (Daneel) + Clarke (HAL) + pop culture archetypes. Each advisor brings a different lens. Collectively smarter than any single perspective.

### HexIsle Three-Realm Trust System (IIFIS)
**Statement:** Skills verification progresses through three realms: Practice (learning) → Stakes (intermediate earning) → Real (verified earning). IIFIS — If It Fits, It Sits — characters physically cannot stand on wrong terrain.
**Why:** Addresses the cold-start trust problem without credentials. IIFIS principle ("make the rule mechanically enforceable at the physics layer") extends to platform design generally: build constraints so bad behavior is literally impossible.

### WildFire Tour Mode
**Statement:** Toggle between demo data and live data across dashboards.
**Why:** Reduces fear of breaking things. Teaches adoption without risk.

### Speckle Garden (Dual-Layer Currency UI)
**Statement:** Gamified frontend on top of compliance-grade backend Credits. Seedling (<100), Sapling (<500), Young Banyan (<2,500), Deep Roots (10,000+).
**Why:** Makes currency feel alive and growing. Banyan metaphor reinforces cooperative values. Compliance hidden; beauty surfaced.

### The Battery (Coordinated Social Dispatch)
**Statement:** Artillery-battery metaphor. ARM/DISARM toggle, FIRE button only when ARMED, "As You Wish" confirmation, 8-platform selection, Intelligence Report preview.
**Why:** Fire all social channels with one command, with safety interlocks. Battery = coordinated firepower.

### Universal Dispatch System
**Statement:** Create once, dispatch everywhere. 15 targets across 4 categories: Social (Twitter, LinkedIn, Bluesky, Threads, Facebook, Instagram, Imgur, Discord), Publications (Medium, Substack), Direct (Email), Platform (Cue Card, Project Update, Beacon Run, Golden Key).
**Why:** Eliminates manual copy-paste. Platform-specific optimizations per target.

### Golden Key System
**Statement:** 15 Golden Keys embedded across 18+ articles via acrostic (Flight tier) or body text (Fledgling tier). Two comprehension quizzes (Scott, Buffett) unlock.
**Why:** Gamified learning. Readers who engage deeply enough to find the keys understand platform philosophy at a cellular level.

### Production Locking
**Statement:** Cost certainty before funding. Creators lock in production costs upfront; funders know exactly what they're paying for.
**Why:** Eliminates the 73% Kickstarter failure rate from cost-estimation errors.

### EOI Credit System
**Statement:** Expression-of-Interest soft commitments accumulate into guaranteed value (purchasing power).
**Why:** Removes the all-or-nothing anxiety of crowdfunding. Converts uncertainty into utility.

---

## V. DIAGNOSTIC VOCABULARY

### The Moneypenny Protocol
**Statement:** Command → Verify-with-Readback → Test. Never trust AI output without regurgitation and ground-truth check.
**Why:** Born from the AI hallucination failure mode. Field-expedient verification (WWII Passphrase) defeats formal protocols.

### Diagnostic Terms
- **Gobbledygook** — AI hallucinated nonsense output.
- **Starscreaming** — catastrophic loop indicator (agent stuck/thrashing).
- **WHEEE!...conk** — near-miss indicator.
- **Vapor Check / WWII Passphrase** — hallucination-breaking technique (ask something only a sane agent could answer).
- **Spin Cycle** — wrong-hypothesis indicator.
- **BOTG (Boots on the Ground)** — override principle: scanner/ground-truth output always beats AI claims.
- **Subtraction Method** — isolation technique via commenting-out.

---

## VI. OPERATING PRINCIPLES

### Slow is Smooth, Smooth is Fast
**Statement:** Military principle. Don't rush. Plan carefully. Deliberate execution beats frantic scrambling.
**Why:** Counter to VC "move fast and break things." Founder built this over nine years on $5K. Slow is viable.

### Necessity IS the Mother of Invention
**Statement:** Innovation from scarcity, not abundance.
**Why:** Founder generated 63–86 innovations in single days during crisis periods. Constraints breed ingenuity. Demonstrates why C+20 scarcity drives innovation harder than VC abundance.

### Anecdotes-as-Proof (Credentials, Not Sob Stories)
**Statement:** Every claim grounded in a Founder anecdote that lived-experienced the principle. Six core anecdotes: Jeep of Theseus, No Brakes, How to Learn to Swim, Intramural Giants, Rooster Tail (Kurt), Christmas Eve 1992.
**Why:** "These aren't sob stories. These are credentials." Real stories as evidence of capability.

### Break Even 500 / Profitable 1,000
**Statement:** Break-even at 500 members (≈ $255K annual burn at current team size). Sustainably profitable at 1,000.
**Why:** Shows feasibility without venture capital. Small team + low burn + member funding = path to profitability that doesn't require extraction or exit.

---

## VII. CULTURAL MARKERS

- **"As You Wish"** — default transaction confirmation phrase (Princess Bride; unconditional assent and delight). Members can customize.
- **"No Atomo. Superman!"** — atom-by-atom no one is Superman. But a community coordinating without hierarchical overhead CAN accomplish superhuman feats. Period then exclamation.
- **"Beacons Are Lit" / "By the Suns of Warvan"** — Lord of the Rings / Galaxy Quest quest-narrative signals. Liana Banyan is an epic, not a startup.
- **"Help each other, help ourselves; let's make that bread."** — Founder's father's blessing. Mutual aid as founding motto.
- **"Veteran of no particular note."** — The Founder's canonical self-description.

---

## VIII. ORIGIN ANCHORS (Biographical)

- **Mr. Cloyd / Sears Lewistown Layaway** → origin of the Voucher System. Cloyd extended $200 credit against young Founder's reputation; lawn-mowing business paid back in two months.
- **USAA Gas Story** → origin of the Courtesy SSL. USAA covered gas when the Founder had $1 in checking.
- **Shape-Note Music Learning** → origin of the Anachronism Principle. Medieval notation taught structured reading that applied to aviation, business, platform.
- **Wife as TasteMaker** → origin of BandWagon. Sampling culture, bringing back good stuff; Founder trusted her judgment "because she has been right so much before."
- **Paper Route Scaling (1 route → 2)** → L0/L1 Dinghy → Skiff proof point in Open Water.
- **Founder's Dad's Principle** → Three-Vendor Model.
- **NextAddress Real Estate Platform** → early platform-building proof.
- **Ravine Wireless ISP Towers** → rural infrastructure proof.
- **26-Country Non-Profit Platform** → global platform-building proof.
- **Liana Banyan Name Origin** → childhood underwater-kingdom memory (mangrove roots) + baobab forest observation (one trunk, many aerial trunks). Etymology: "banyan" = merchant/trading caste. Mutualism with interlocking roots provides protection against economic hostility.
- **Mike Puckett (Free Pizza Dude)** → Pizza Angel cold-start pipeline; Nashville beachhead. Fed 4,000+ people via PayPal + Imgur. His model proves community-scale mutual aid works.

---

## IX. DRIFT / TENSION RESOLUTIONS (B108 — ratified by Founder unless flagged PENDING)

1. **IP split — RESOLVED.** Canonical: **60/20/10/10**. Treat 60/20/20 as stale on sight. (Founder confirmed B108.)
2. **Innovation count — RESOLVED.** Canonical: **2,265**. Verified against Supabase `innovation_log` table (B108, content-range `0-4/2265`, highest innovation_number = 2265). `canonical_values.yaml` is **stale at 2,263** — two behind. The YAML must be updated; flagged as a Scrambler finding for Knight.
3. **Boaz Principle % — RECOMMENDATION PENDING FOUNDER RATIFICATION.** Two-tier proposal:
   - **3.3% structural baseline** (Talmudic 1/30 of harvest; arithmetically elegant as one-fifth of the 16.7% platform take). Flows automatically to newcomer benefit pool every transaction.
   - **Optional corner bonuses 5% / 10% / 15%** (Bronze / Silver / Gold Benefactor tiers) — voluntary stacking at campaign level above the 3.3% floor.
   This reconciles both archive numbers found ("3.3%" specific and "5–15% range") as two layers of a single system.
4. **Cost+20 expression — NOT A CONFLICT.** "20% margin over cost" and "16.7% of final price" are the same mathematical statement (1/1.20 = 0.833…). Use whichever fits the audience.
5. **Eleven vs Twenty vs Nineteen laws — RESOLVED via three-tier taxonomy (Section I).** These are not competing lists; they are different *views* of one underlying framework:
   - **Master canonical** (Section I above): 8 Constitutional + 4 Mathematical + 7 Behavioral = **19 laws**, explicitly taxonomized.
   - **"Eleven Economic Laws of the Keep"** (from `economicLawsCueCards.ts`): teaching subset for member onboarding. Mostly Tier 3 behavioral (because members relate to behavior). Curated from the master.
   - **"Twenty Laws of C+20"** (from `ARCHIVE2/twenty-laws-of-c20.md`): academic paper view, split into 9 mathematical + 11 behavioral. Maps onto Tier 2 + Tier 3 of the master taxonomy.
   Forward rule: if any view adds a law not in the master, update the master first. The master is the source of truth; the "Eleven" and "Twenty" are derived publications.
6. **Scott letter anchor metaphor — RESOLVED.** Canonical: **"Cardboard Boots"** (NOT "Flight of the Phoenix" — old variant, stale).

---

## X. CROWN LETTER CONTEXT (LOCKED versions — canonical)

Each Crown Letter has a LOCKED canonical version. When a new session produces a "cleaner" version that silently undoes prior editorial decisions (headerless flow, specific placement of the military passage, "Especially from friendly fire" fragment, mixed contractions, Dar es Salaam specificity), that new version is **stale** — the LOCKED version wins until the Founder explicitly ratifies an update.

Current LOCKED Crown Letters:

- **MacKenzie Scott** → `CROWN_LETTER_MACKENZIE_SCOTT_BOARD_CHAIR` (LOCKED02, Feb 10). Current active draft: v004 (B107) under review. Anchor metaphor: **Cardboard Boots**.
- **Michael Seibel** → LOCKED02 (CEO offer). Used as reference source for Press Junket / Sponsor-tier access language.
- **Craig Newmark** → `LOCKED01_CROWN_LETTER_CRAIG_NEWMARK_INFRASTRUCTURE_CHANCELLOR.md` (Feb 12). Crown title: **Infrastructure Chancellor**. Signature editorial decisions preserved:
  - Headerless continuous-prose flow (matches Craigslist sensibility)
  - Military passage woven into the Ask, not siloed in "Who I Am"
  - Dar es Salaam + "torrentially" specificity in Africa paragraph
  - "Especially from friendly fire" standalone fragment
  - Mixed contractions (intentional voice)
  - P.S. references the Three Original Economic Inventions without naming them
  - `@craignewmarkphilanthropies.org` email personalization in Red Carpet line
  - Bus-driver chain-reaction paragraph cut (lives in Scott letter to avoid cross-letter redundancy)
  - "Nothing about us without us" cut (redundant with Scott)
  A LOCKED03 version exists that undid most of these. LOCKED03 is **stale** — LOCKED01 is canonical.

**General Crown Letter rules** (drawn from the Newmark iteration experience):
- Letters are often read together on Cephas. Avoid cross-letter redundancy.
- The Scott letter owns: bus-driver chain reaction, "nothing about us without us" framing, eight kids mention, Board Chair Crown.
- Each letter's military passage should be *operationally necessary* (earning its place by explaining why the ask is what it is), not biographical.
- The Press Junket / $5,000 Sponsor-tier standing offer is in multiple letters but framed per recipient.
- Each letter names the other Crown recipients (Scott / Seibel / Simon / Khan / Andrés) so recipients see the ecosystem forming — not five separate asks.

**Twelve SEC-clean Crown Letter recipients:** Buffett, Scott, Khan, Newmark, Seibel, Simon, Dougherty, Glenn, Williams, Kaiser, Trebor Scholz, Oliver Scholz. On indefinite hold: Gates (Epstein association).

---

## XI. DOCUMENT MAINTENANCE RULES

1. **Any new law, principle, or framework introduced in a session MUST be added to this document before session close.** Otherwise it dissipates.
2. **Any conflict between this document and a letter / paper / pudding / innovation writeup — THIS DOCUMENT WINS** until Founder ratifies an update.
3. **Updates must preserve prior language in the Origin Reasoning section** — new framings are additions, not replacements, unless explicitly retired.
4. **Version: this document replaces any prior "economic laws" or "canonical principles" document.** Earlier copies should be archived with a pointer here.

---

*Compiled B108 · April 18, 2026 · Bishop Foreman · For the R9 Preload · For the Keep*
