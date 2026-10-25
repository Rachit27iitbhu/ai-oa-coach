import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="AI OA Coach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Sarvam AI Client
# Initialize Sarvam AI Client
def get_sarvam_client():
    api_key = os.getenv("SARVAM_API_KEY") or st.session_state.get("user_api_key")
    if api_key and api_key != "your_sarvam_api_key_here":
        try:
            from sarvamai import SarvamAI  # Corrected class name
            return SarvamAI(api_subscription_key=api_key)  # Corrected parameter name
        except Exception as e:
            st.error(f"Failed to initialize Sarvam Client: {e}")
            return None
    return None

# Sample Problems for Demo
SAMPLE_PROBLEMS = {
    "C++: Two Sum (Array / Hash Map)": {
        "lang": "C++",
        "code": """// Problem: Given an array of integers `nums` and an integer `target`, 
// return indices of the two numbers such that they add up to target.
// Target: 9
// nums = [2, 7, 11, 15]

#include <vector>
#include <unordered_map>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> mp;
    for(int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if(mp.count(complement)) return {mp[complement], i};
        mp[nums[i]] = i;
    }
    return {};
}"""
    },
    "C++: Sliding Window Maximum": {
        "lang": "C++",
        "code": """// Problem: Find the maximum element in each sliding window of size k in an array.
// Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
// Output: [3,3,5,5,6,7]

#include <vector>
#include <deque>
using namespace std;

vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;
    vector<int> ans;
    for(int i = 0; i < nums.size(); i++) {
        if(!dq.empty() && dq.front() == i - k) dq.pop_front();
        while(!dq.empty() && nums[dq.back()] < nums[i]) dq.pop_back();
        dq.push_back(i);
        if(i >= k - 1) ans.push_back(nums[dq.front()]);
    }
    return ans;
}"""
    },
    "SQL: Second Highest Salary with NULLs & Duplicates": {
        "lang": "SQL",
        "code": """-- Problem: Find the second highest distinct salary from the Employee table.
-- If there is no second highest salary, return NULL.
-- Table: Employee (id INT, salary INT)

SELECT (
    SELECT DISTINCT salary 
    FROM Employee 
    ORDER BY salary DESC 
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;"""
    },
    "SQL: Cumulative Monthly Revenue & NULL Handling": {
        "lang": "SQL",
        "code": """-- Problem: Calculate cumulative monthly revenue for each store.
-- Handle missing/NULL revenues by replacing them with 0.
-- Table: Sales (store_id INT, sale_date DATE, amount DECIMAL)

SELECT 
    store_id,
    DATE_FORMAT(sale_date, '%Y-%m') AS month,
    SUM(COALESCE(amount, 0)) OVER (
        PARTITION BY store_id 
        ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
    ) AS cumulative_revenue
FROM Sales;"""
    }
}

# Sidebar Settings
st.sidebar.title("⚡ AI OA Coach")
st.sidebar.markdown("---")

api_key_input = st.sidebar.text_input(
    "Sarvam API Key:",
    type="password",
    value=os.getenv("SARVAM_API_KEY", ""),
    help="Paste your Sarvam API Key here or set it in .env"
)
if api_key_input:
    st.session_state["user_api_key"] = api_key_input

client = get_sarvam_client()
if client:
    st.sidebar.success("🟢 Sarvam AI Connected")
else:
    st.sidebar.warning("🟡 Demo Mode Active (No Key)")

st.sidebar.markdown("---")
selected_sample = st.sidebar.selectbox("Load Sample Problem:", ["Custom Input"] + list(SAMPLE_PROBLEMS.keys()))

# Main Header
st.title("🎯 AI Online Assessment Coach")
st.caption("Master programming interview problems & SQL online assessments with guided hints, edge case analysis, and error reviews.")

# Tabs Layout
tab_input, tab_pattern, tab_hints, tab_cases, tab_review, tab_practice = st.tabs([
    "📝 Problem & Code", 
    "🔍 Pattern & Clues", 
    "💡 Progressive Hints", 
    "🧪 Edge Cases", 
    "🚨 Solution Review & Complexity", 
    "🏋️ Focused Practice"
])

# Code Input Logic
if selected_sample != "Custom Input":
    default_lang = SAMPLE_PROBLEMS[selected_sample]["lang"]
    default_code = SAMPLE_PROBLEMS[selected_sample]["code"]
else:
    default_lang = "C++"
    default_code = ""

with tab_input:
    col1, col2 = st.columns([1, 3])
    with col1:
        lang = st.selectbox("Select Language", ["C++", "SQL"], index=0 if default_lang == "C++" else 1)
    with col2:
        st.info(f"Targeting: **{lang}** Online Assessment Preparation")

    problem_code = st.text_area("Paste Problem Description / Your Solution:", value=default_code, height=300)

# Helper Function to query Sarvam API or output mock response
# Helper Function to query Sarvam API or output mock response
# Helper Function to query Sarvam API or output mock response
def generate_coaching_response(prompt: str, fallback_response: str) -> str:
    if client:
        try:
            with st.spinner("Sarvam AI analyzing..."):
                response = client.chat.completions(
                    model="sarvam-105b",  # or "sarvam-2b"
                    messages=[
                        {"role": "system", "content": "You are an expert OA (Online Assessment) coach for C++ and SQL interviews."},
                        {"role": "user", "content": prompt}
                    ]
                )
                # Safely extract content and ensure it's not None
                if response and response.choices and response.choices[0].message:
                    content = response.choices[0].message.content
                    if content:
                        return str(content)
        except Exception as e:
            st.error(f"Sarvam API Error: {e}. Falling back to demo response.")
            
    return fallback_response

# Tab 1: Pattern & Clues
with tab_pattern:
    st.subheader("🔍 Identified Problem-Solving Pattern")
    if st.button("Analyze Pattern & Clues", key="btn_pattern"):
        if not problem_code.strip():
            st.warning("Please paste code or a problem statement first.")
        else:
            prompt = f"Identify the problem-solving pattern and explain the clues for this {lang} problem:\n\n{problem_code}"
            fallback = f"### Identified Pattern ({lang})\n" + (
                "**Pattern:** Hash Map / Frequency Array Lookup\n\n"
                "**Key Clues:**\n"
                "- Need to find pairs in $O(N)$ time complexity.\n"
                "- Looking for complementary values (`target - x`).\n"
                "- Requires fast key-value retrieval." if lang == "C++" else 
                "**Pattern:** Window Functions & Aggregation with NULL safety\n\n"
                "**Key Clues:**\n"
                "- `DISTINCT` keyword handles duplicate rows.\n"
                "- `COALESCE` handles `NULL` missing value returns.\n"
                "- `OFFSET` / `LIMIT` isolates target rank."
            )
            res = generate_coaching_response(prompt, fallback)
            st.markdown(res)

# Tab 2: Progressive Hints
with tab_hints:
    st.subheader("💡 Guided Hints (No Spoilers)")
    if st.button("Get Progressive Hints", key="btn_hints"):
        if not problem_code.strip():
            st.warning("Please paste code or a problem statement first.")
        else:
            prompt = f"Provide 3 progressive hints for this {lang} problem. Do NOT reveal the full solution.\n\n{problem_code}"
            fallback = """
**Hint 1 (High Level):** Think about what state or history you need to store as you iterate.
**Hint 2 (Data Structure):** How can you check if an element has been seen before in $O(1)$ time?
**Hint 3 (Edge Cases):** Consider what happens when the array/table is empty, contains duplicate values, or has NULL entries.
"""
            res = generate_coaching_response(prompt, fallback)
            st.markdown(res)

# Tab 3: Edge Cases
with tab_cases:
    st.subheader("🧪 Crucial Edge Cases & Test Scenarios")
    if st.button("Generate Edge Cases", key="btn_cases"):
        if not problem_code.strip():
            st.warning("Please paste code or a problem statement first.")
        else:
            prompt = f"Generate critical edge cases and explain what each case tests for this {lang} solution:\n\n{problem_code}"
            fallback = f"### Critical Edge Cases ({lang})\n" + (
                "1. **Empty / Minimal Input:** Single element array `[5]`, target = 5. Tests boundary check.\n"
                "2. **Negative Numbers:** `[-3, 4, 3, 90]`, target = 0. Tests arithmetic handling.\n"
                "3. **Duplicate Values:** `[3, 3]`, target = 6. Tests hash collision or key overwriting." if lang == "C++" else
                "1. **All Duplicate Salaries:** All rows have $10,000. Tests `DISTINCT` condition.\n"
                "2. **Empty Table / Less than K Rows:** Only 1 employee present. Tests NULL output behavior.\n"
                "3. **NULL Values in Column:** Salary column contains `NULL`. Tests missing value handling."
            )
            res = generate_coaching_response(prompt, fallback)
            st.markdown(res)

# Tab 4: Review & Complexity
with tab_review:
    st.subheader("🚨 Solution Review, Pitfalls & Complexity Analysis")
    if st.button("Review Code & Complexity", key="btn_review"):
        if not problem_code.strip():
            st.warning("Please paste code or a problem statement first.")
        else:
            prompt = f"Review this {lang} solution for logical errors, common incorrect approaches, and analyze time/space complexity:\n\n{problem_code}"
            fallback = f"### Solution Review ({lang})\n\n" + (
                "**Time Complexity:** $\mathcal{O}(N)$ - Single pass through the input array.\n"
                "**Space Complexity:** $\mathcal{O}(N)$ - Hash map stores up to $N$ elements.\n\n"
                "**Common Pitfalls:**\n"
                "- Using nested loops resulting in $\mathcal{O}(N^2)$ Time Limit Exceeded (TLE).\n"
                "- Re-using the same element at the same index twice." if lang == "C++" else
                "**Query Evaluation Performance:** Efficient indexing needed on filter/grouping columns.\n\n"
                "**Common Pitfalls:**\n"
                "- Forgetting `DISTINCT`, causing duplicate values to skew ranking.\n"
                "- Failing to handle empty query results with `COALESCE` or outer query wrapping."
            )
            res = generate_coaching_response(prompt, fallback)
            st.markdown(res)

# Tab 5: Practice Exercise
with tab_practice:
    st.subheader("🏋️ Recommended Follow-up Practice")
    if st.button("Get Recommended Exercise", key="btn_practice"):
        if not problem_code.strip():
            st.warning("Please paste code or a problem statement first.")
        else:
            prompt = f"Recommend one focused follow-up exercise related to this {lang} problem:\n\n{problem_code}"
            fallback = f"### Follow-up Practice Problem ({lang})\n" + (
                "**Recommended Exercise:** *3Sum (Three Sum)*\n"
                "- **Goal:** Find all unique triplets in the array that sum to zero.\n"
                "- **Why:** Builds upon Two-Sum concepts by combining two-pointer technique with duplicate elimination." if lang == "C++" else
                "**Recommended Exercise:** *Nth Highest Salary / Rank Scores*\n"
                "- **Goal:** Generalize the query to find the $N$-th highest salary using `DENSE_RANK()` or window functions.\n"
                "- **Why:** Strengthens SQL ranking function knowledge under real test scenarios."
            )
            res = generate_coaching_response(prompt, fallback)
            st.markdown(res)