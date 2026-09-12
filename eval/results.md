# Evaluation Report: ChatRecall Semantic Retrieval Performance

## 1. Executive Summary

This report presents a rigorous, honest evaluation of **ChatRecall** against traditional **BM25 Lexical Keyword Search** across a 4,482-message synthetic group chat archive spanning 6 months (8 participants, Hinglish code-mixing, and 3 long resolving decision threads).

The test suite consists of **40 ground-truth queries**, containing **10 strictly verified Zero-Word-Overlap ("Hard") queries** where the user query and the target message share zero common words.

---

## 2. Core Benchmark Results

| Metric Slice | Query Count | ChatRecall Top-1 Acc | ChatRecall Top-3 Acc | ChatRecall MRR | BM25 Top-1 Acc | BM25 Top-3 Acc | BM25 MRR |
|---|---|---|---|---|---|---|---|
| **Overall (All Queries)** | **40** | **72.5%** | **80.0%** | **0.7771** | 35.0% | 50.0% | 0.4348 |
| **🔥 Hard (Zero-Word-Overlap)** | **10** | **60.0%** | **80.0%** | **0.7** | **0.0%** | **0.0%** | **0.0** |
| **Baseline (Warmup Queries)** | **30** | **76.67%** | **80.0%** | **0.8028** | 46.67% | 66.67% | 0.5798 |

---

## 3. The Honest Accuracy Gap Analysis

### 3.1 The Zero-Word-Overlap Collapse of Keyword Search
- **BM25 Keyword Search fails completely on Zero-Word-Overlap queries (0.0% Top-1 Accuracy, 0.0000 MRR)**.
- When a user asks *"When did we decide on the mountain holiday?"* and the target message is in Hinglish (*"Chalo sab lock ho gaya: Manali trip finalized for Dec 28 to Jan 2!"*), text search cannot bridge the conceptual gap between *mountain holiday* and *Manali*.
- **ChatRecall achieves 60.0% Top-1 Accuracy (80.0% Top-3)** on these exact zero-word-overlap queries through multilingual embedding space alignment and decision boosting.

### 3.2 The Performance Gap
- **Overall Accuracy vs Hard Accuracy**:
  - ChatRecall Top-1 Accuracy: 72.5% (Overall) vs 60.0% (Hard).
  - Accuracy Gap: **12.5%**.
- The slight gap arises from nuanced semantic ambiguities (e.g. distinguishing between multiple discussion messages in a thread before the final decision).

---

## 4. Breakdown by Category & Query Shape

| Category | Count | ChatRecall Top-1 | ChatRecall Top-3 | ChatRecall MRR | BM25 Top-1 | BM25 MRR |
|---|---|---|---|---|---|---|
| **Decision Retrieval** | 3 | 66.67% | 66.67% | 0.6667 | 0.0% | 0.1667 |
| **General Semantic** | 7 | 100.0% | 100.0% | 1.0 | 71.43% | 0.8571 |
| **Person Filter (Ananya)** | 2 | 100.0% | 100.0% | 1.0 | 100.0% | 1.0 |
| **Person Filter (Priya)** | 2 | 100.0% | 100.0% | 1.0 | 0.0% | 0.25 |
| **Person Filter (Rohan)** | 2 | 100.0% | 100.0% | 1.0 | 100.0% | 1.0 |
| **Person Filter (Tanvi)** | 2 | 100.0% | 100.0% | 1.0 | 100.0% | 1.0 |
| **Person Filter (Vikram)** | 2 | 100.0% | 100.0% | 1.0 | 50.0% | 0.5714 |
| **Time Filter (December 2023)** | 1 | 0.0% | 0.0% | 0.0 | 0.0% | 0.0 |
| **Time Filter (Diwali Nov 2023)** | 1 | 0.0% | 0.0% | 0.1667 | 0.0% | 0.0 |
| **Time Filter (January 2024)** | 2 | 50.0% | 50.0% | 0.625 | 0.0% | 0.25 |
| **Time Filter (Last Month / Feb 2024)** | 1 | 0.0% | 0.0% | 0.0 | 0.0% | 0.0 |
| **Time Filter (March 2024)** | 2 | 100.0% | 100.0% | 1.0 | 100.0% | 1.0 |
| **Time Filter (November 2023)** | 2 | 50.0% | 100.0% | 0.75 | 0.0% | 0.25 |
| **Time Filter (October 2023)** | 1 | 0.0% | 0.0% | 0.1667 | 0.0% | 0.25 |
| **Zero-Word Overlap (Commute)** | 1 | 0.0% | 100.0% | 0.5 | 0.0% | 0.0 |
| **Zero-Word Overlap (Decision)** | 3 | 100.0% | 100.0% | 1.0 | 0.0% | 0.0 |
| **Zero-Word Overlap (Decor)** | 1 | 100.0% | 100.0% | 1.0 | 0.0% | 0.0 |
| **Zero-Word Overlap (Events)** | 1 | 0.0% | 100.0% | 0.5 | 0.0% | 0.0 |
| **Zero-Word Overlap (Finance)** | 1 | 0.0% | 0.0% | 0.0 | 0.0% | 0.0 |
| **Zero-Word Overlap (Food & Routine)** | 1 | 0.0% | 0.0% | 0.0 | 0.0% | 0.0 |
| **Zero-Word Overlap (Rules)** | 1 | 100.0% | 100.0% | 1.0 | 0.0% | 0.0 |
| **Zero-Word Overlap (Smart Home)** | 1 | 100.0% | 100.0% | 1.0 | 0.0% | 0.0 |

---

## 5. Detailed Query-by-Query Evaluation Log

| ID | Query | Target ID | Hard? | Strategy | Rank | Result Status |
|---|---|---|---|---|---|---|
| Q01 | When did we decide on the mountain holiday? | `MSG_00979` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q02 | Surprise reading gadget ordered for our friend moving abroad | `MSG_03727` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q03 | What was the agreed upfront tenancy caution fund? | `MSG_02259` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q04 | What is the penalty for skipping exercise streak? | `MSG_02056` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q05 | Who is carpooling to the IT hub by automobile? | `MSG_02995` | 🔥 Yes | `semantic` | 2 | ⚠️ Top-2 |
| Q06 | How to reduce income levy before fiscal close? | `MSG_03427` | 🔥 Yes | `semantic` | N/A | ❌ Miss |
| Q07 | Traditional attire festive dinner gathering | `MSG_00899` | 🔥 Yes | `semantic` | 2 | ⚠️ Top-2 |
| Q08 | Morning beverage preference after park jog | `MSG_00046` | 🔥 Yes | `semantic` | N/A | ❌ Miss |
| Q09 | Programmed residential water boiler countdown switch | `MSG_00096` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q10 | Illuminations and audio equipment for celebration | `MSG_00894` | 🔥 Yes | `semantic` | 1 | ✅ Top-1 |
| Q11 | What did Priya say about the budget? | `MSG_00689` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q12 | Priya's advice on buying flight tickets | `MSG_02838` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q13 | Did Vikram report an internet broadband outage ticket? | `MSG_01030` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q14 | What did Vikram say about mechanical keyboard? | `MSG_00608` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q15 | Rohan's message about airport cab booking | `MSG_01528` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q16 | What did Rohan share for weekend trekking in Coorg? | `MSG_02557` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q17 | Ananya's vintage denim jacket thrift store find | `MSG_00355` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q18 | What pottery workshop did Ananya mention? | `MSG_00759` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q19 | Tanvi cab driver assignment details | `MSG_03146` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q20 | Did Tanvi get confirmation from Airbnb host for early check-in? | `MSG_02196` | No | `person_filtered` | 1 | ✅ Top-1 |
| Q21 | What did we discuss in December regarding advance tax? | `MSG_01394` | No | `time_filtered` | N/A | ❌ Miss |
| Q22 | What did we discuss around Diwali? | `MSG_00891` | No | `time_filtered` | 6 | ❌ Miss |
| Q23 | What happened in January regarding gym and fitness resolutions? | `MSG_02053` | No | `time_filtered` | 1 | ✅ Top-1 |
| Q24 | What did we discuss in January about flat lease and rent negotiation? | `MSG_02259` | No | `time_filtered` | 4 | ❌ Miss |
| Q25 | What did we discuss last month regarding carpool to office? | `MSG_02995` | No | `time_filtered` | N/A | ❌ Miss |
| Q26 | Discussions in March about Section 80C investment proofs | `MSG_03426` | No | `time_filtered` | 1 | ✅ Top-1 |
| Q27 | Farewell planning in March for Siddharth | `MSG_03708` | No | `time_filtered` | 1 | ✅ Top-1 |
| Q28 | Discussions in November about New Year vacation destinations | `MSG_00951` | No | `time_filtered` | 1 | ✅ Top-1 |
| Q29 | What did we discuss in October about Bangalore Metro Purple line? | `MSG_00001` | No | `time_filtered` | 6 | ❌ Miss |
| Q30 | New Year trip dates discussion in November | `MSG_00960` | No | `time_filtered` | 2 | ⚠️ Top-2 |
| Q31 | What was the final decision for the winter trip? | `MSG_00979` | No | `semantic` | 1 | ✅ Top-1 |
| Q32 | What was the finalized rent and security deposit for the 3BHK flat? | `MSG_02259` | No | `semantic` | 1 | ✅ Top-1 |
| Q33 | What gift and dinner venue were finalized for Siddharth's farewell? | `MSG_03727` | No | `semantic` | N/A | ❌ Miss |
| Q34 | Who is going to the hospital emergency night shift duty? | `MSG_01439` | No | `semantic` | 1 | ✅ Top-1 |
| Q35 | Who bought tickets for Friday night first day first show movie at PVR? | `MSG_03211` | No | `semantic` | 1 | ✅ Top-1 |
| Q36 | Who received a traffic police fine for unstrapped helmet? | `MSG_02449` | No | `semantic` | 1 | ✅ Top-1 |
| Q37 | Who was stuck in heavy Silk Board traffic jam? | `MSG_01317` | No | `semantic` | 1 | ✅ Top-1 |
| Q38 | Who makes authentic South Indian filter coffee with chicory blend? | `MSG_00467` | No | `semantic` | 1 | ✅ Top-1 |
| Q39 | What board games were brought for the party? | `MSG_00895` | No | `semantic` | 1 | ✅ Top-1 |
| Q40 | Who celebrated Swiggy Instamart delivery in 7 minutes? | `MSG_01665` | No | `semantic` | 1 | ✅ Top-1 |

---

## 6. Latency & System Throughput
- **Total evaluation runtime**: 3.77 seconds for 40 multi-strategy queries (avg: ~94.3 ms/query).
- **Index Scale**: 4,482 messages, 384-dimensional dense vectors with instantaneous dot product matching.
