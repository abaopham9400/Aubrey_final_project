# Individual Contribution: Guide RNA Designer Module
**Course:** BioE234 - Bioengineering Automation  
**Project Component:** Stage 1 — CRISPR gRNA Selection, Scoring, and Design

## 1. Overview & Project Narrative
In our team's end-to-end CRISPR Experiment Assistant, my role is to design the algorithm that finds the best gRNA. While my teammates handle initial experiment parameters and downstream validation, my module performs the core bioinformatic computation. 

My pipeline takes a biological target (either a gene name or a raw DNA sequence), identifies all viable CRISPR-Cas9 cutting sites, and applies a scoring algorithm to rank these sites based on experimental efficiency and safety.

## 2. My Contributions
I have developed a suite of five interconnected tools that form a robust gRNA design engine. Each tool is has a MCP wrapper, allowing Gemini to chain them together to solve complex user requests.

### Core Logic Scripts (`.py`)
| File | Functionality |
| :--- | :--- |
| `validate_DNA.py` | Sanitizes and validates input sequences to ensure they only contain {A, T, C, G} before processing. |
| `find_pam.py` | Scans both the **sense and anti-sense** strands of the target DNA for the `NGG` PAM. |
| `find_protospacer.py` | Extracts the 20bp target sequence upstream of each identified PAM site. |
| `calculate_score.py` | **The Scoring Engine.** Evaluates gRNAs based on GC content (40-60%), penalizes Poly-T (`TTTT`), and flags off-targets. |
| `design_cas9_RNA.py` | The master function that integrates all sub-tools to return a finalized sgRNA structure. |

### MCP Integration (`.json`)
For every script above, I created a corresponding `.json` wrapper (e.g., `calculate_score.json`). These files define the schema that Gemini uses to understand the required inputs, data types, and keywords that trigger the tool during a natural language conversation.

## 3. LLM Training & Prompt Engineering
A major part of my contribution was developing natural language prompts to guide the LLM's decision-making. These prompts (found in my test suites and design docs) train the LLM to:
1.  **Identify Intent:** Recognize when a user wants a "safe" guide vs. a "highly efficient" guide.
2.  **Chain Tools:** Understand that it must call `find_pam` before it can `calculate_score`.
3.  **Handle Gene Names:** Efficiently move from a name like *TP53* to a ranked list of guides by orchestrating my sequence validation and scoring tools.

## 4. How to Evaluate My Work
To see my contributions in action, the professor can follow this path:
1.  **Unit Tests:** Run `pytest test_calculate_score.py` (or equivalent) to see the scoring logic in action.
2.  **Logic Flow:** Review `find_pam.py` to see index detection, then `calculate_score.py` for the bioinformatic math.
3.  **End-to-End:** Invoke the `design_cas9_RNA` tool; it demonstrates the full integration of my sub-functions into a single usable result.

---
**Summary of Technical Skills:**
* **Bioinformatics:** Pattern matching (PAM), GC calculation, and sequence manipulation.
* **Software Engineering:** MCP implementation and modular Python programming.
* **Prompt Engineering:** Designing context-aware instructions for LLM tool-calling.
