# AI Workflow Architecture: Weekly Product Pulse

This prototype automates the analysis of user reviews to generate internal product updates and standardized fee explanations for **INDmoney**, using the **AI Engine** and **Model Context Protocol (MCP)** patterns.

## 🚀 Features
- **PII Scrubbing:** Automatically removes names, emails, and phone numbers from reviews before processing.
- **Weekly Pulse Generation:** Clusters reviews into themes and identifies action ideas using `llama-3.1-70b`.
- **Fee Explainer:** Generates neutral, bulleted explanations for complex fee scenarios (e.g., Exit Load) using `llama-3.1-8b`.
- **Approval-Gated Actions:** Uses MCP-style tool execution to:
  - Append reports to a Master Notes document.
  - Create email drafts for the support/product teams.

### Stage 3: AI Intelligence

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   - Rename `.env.example` to `.env`.
   - Add your [AI API Key](https://console.groq.com/keys).

3. **Generate Sample Data:**
   ```bash
   python generate_data.py
   ```

4. **Launch the UI Dashboard:**
   ```bash
   streamlit run app.py
   ```

5. **Run via CLI (Alternative):**
   ```bash
   python main_workflow.py
   ```

## 🛡️ MCP & Approval Gating
All external actions are strictly gated. In the UI, use the **Actions** section to:
- **`Approve & Append to Notes`**: Writes to `MASTER_NOTES.md`.
- **`Approve & Draft Email`**: Saves a .txt draft in `email_drafts/`.
- **`Download One-Pager PDF`**: Generates a clean PDF summary of the report.

## 📄 Fee Scenario Covered
**Scenario:** Exit Load on Mutual Funds
- Covers how INDmoney handles exit loads for different fund categories.
- Includes neutral facts regarding the 1% charge for early withdrawals (typically <1 year).

## 🔗 Sources Used
1. [INDmoney Help Center - Exit Loads](https://www.indmoney.com/help/mutual-funds/what-is-exit-load)
2. [SEBI Guidelines on Mutual Fund Charges](https://www.sebi.gov.in/legal/circulars/oct-2018/circular-on-ter-and-performance-disclosure_40774.html)
3. [AMFI - Understanding Exit Load](https://www.amfiindia.com/investor-corner/knowledge-center/exit-load.html)
4. [INDmoney Pricing Page](https://www.indmoney.com/pricing?type=mutual-funds)
