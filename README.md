# ⚡ AI Online Assessment Coach

An interactive, AI-powered Online Assessment (OA) and coding interview prep platform built with **Streamlit** and **Sarvam AI**. 

Designed specifically for **C++** and **SQL** interview preparation, this tool helps users break down complex programming problems through structured pattern recognition, progressive hints, edge case analysis, code reviews, and targeted follow-up practice.

---

## 🚀 Key Features

- **🔍 Pattern Recognition & Clues:** Identifies core algorithmic patterns (e.g., Two-Pointer, Hash Map, Window Functions, Group By) and highlights key problem indicators.
- **💡 Progressive Hints:** Provides step-by-step guidance without spoiling the complete solution.
- **🧪 Edge Case Generator:** Highlights potential failure scenarios (minimal inputs, duplicates, `NULL` values) and explains what each case tests.
- **🚨 Solution Review & Complexity:** Audits submitted code for logical flaws, common pitfalls, and provides time/space complexity analysis ($O(N)$, $O(1)$, etc.).
- **🏋️ Targeted Follow-up Practice:** Suggests relevant exercises to reinforce concept mastery.
- **⚡ Dual Engine (Live AI + Offline Demo Mode):** Integrates Sarvam AI models while offering a fully operational demo mode with built-in realistic sample problems when offline or without an API key.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **AI Model Integration:** [Sarvam AI SDK](https://docs.sarvam.ai/) (`sarvam-105b` / `sarvam-2b`)
- **Environment Management:** `python-dotenv`
- **Language Support:** C++, SQL

---

## 📁 Repository Structure

```text
.
├── .env                  # Environment variables (API Key)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Project dependencies
├── app.py                # Main Streamlit application
└── README.md             # Project documentation
