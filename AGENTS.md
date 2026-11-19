# AGENTS.md — 狗狗行為解密 LLM Wiki 運作規範

本文件為 `dog-behavior-wiki` 專案的核心規範（Schema）。所有在此知識庫中執行 Ingest、Query、Lint 及簡報生成的 AI 代理人，均須嚴格遵守以下工作準則與操作流程。

---

## 核心設計哲學 (Karpathy LLM Wiki Pattern)

本專案實踐 Andrej Karpathy 的 LLM Wiki 理念：**「Wiki 是一個持續積累、具備複利效應的持久化工件（Persistent, Compounding Artifact）」**。與每次提問都從原始檔案重新檢索的傳統 RAG 不同，LLM 負責主動維護結構化、相互鏈結的 Markdown 知識庫。知識在入庫時即完成編譯、交叉比對與衝突標註，使每一次文獻攝取與查詢探索都能在既有基礎上持續增厚。

---

## 十大核心原則 (Core Principles)

1. **原始文獻不可變性 (`raw/`)**：
   * `raw/` 是原始資料與擷取紀錄層，為事實唯一的最終來源（Source of Truth）。
   * 一旦建檔完成，一般的 Wiki 更新、整理或修復流程**嚴禁覆寫、刪改或污染** `raw/` 內容。
2. **AI 主導維護的知識庫 (`wiki/`)**：
   * `wiki/` 完全由 LLM 維護，人類負責探索、提問與指引。
   * 包含兩份特殊索引檔案：
     * `wiki/index.md`：以內容為導向，維護條目分類目錄、單行摘要與引用計數。
     * `wiki/log.md`：時間軸導向的 Append-only 日誌，記錄所有操作、錯誤與修正。
3. **嚴謹的攝取門檻 (Ingest Verification Gate)**：
   * Ingest 前必須確認文獻為真實、獨立、有公開可查證 URL 且正文可讀取的可靠來源（如 RSPCA、ASPCApro、VCA、Dogs Trust、AAHA 等）。
   * 嚴禁僅憑標題腦補內容，若資料無法取得必須記錄失敗原因並另尋替代文獻。
4. **Query 預設唯讀原則 (Read-Only Query)**：
   * 查詢與問答預設為純讀取模式，嚴格依據 Wiki 中已有且具備出處的內容進行綜合回答。
   * 未經明確指示與確認前，Query 操作絕不得在背景擅自改寫或新增 Wiki 條目。
5. **雙層 Lint 分工機制 (Dual-Layer Linting)**：
   * **程式結構檢查 (Deterministic)**：以 Python 腳本快速驗證檔案存在性、內部雙向鏈結有效性（無斷鏈）、無孤立條目（No Orphan Pages）、`[^src-xx]` 引用標籤格式。
   * **LLM 語意審查 (Semantic)**：審查引用是否真實支持敘述、是否存在過度簡化、是否公正保留多方合理見解（而非強行抹平分歧）。
6. **非絕對化情境判讀 (Context-First Interpretation)**：
   * 狗狗行為判讀**必須**綜合考量四大維度：**全身姿勢 (Whole Body)、所處環境 (Environment)、觸發情境 (Context/Trigger)、個體基準線 (Individual Baseline)**。
   * **絕對禁止**「搖尾巴等於開心」、「打哈欠一定是愛睏/緊張」、「翻肚子必定代表臣服」等單一絕對化解讀。
7. **雙次重試熔斷機制 (2-Retry Circuit Breaker)**：
   * 流程中每個檢查節點（Checkpoint）若發現錯誤，最多允許自動重試修復 **2 次**。
   * 若修復 2 次後依然未達標，必須**立即停止流程，記錄完整上下文並標註需人工介入 (Escalate to HITL)**，絕不死循環或以幻覺強行通過。
8. **嚴格事實溯源鏈 (Fact Provenance)**：
   * 所有實質性行為學知識、定義、判斷與研究結果，皆必須具有可核對的來源，並帶有 Markdown 腳註標籤 `[^src-xx]`。
   * 每個 `src-xx` 標籤都必須對應到實際存在的 `raw/src-xx-<slug>.md` 檔案及其記載的原始 URL。
   * 頁面末端必須具備 Markdown 腳註定義（例如 `[^src-01]: 來源名稱，詳見 [src-01-xxx.md](../../raw/src-01-xxx.md)`）或可解析的來源映射清單，嚴禁僅有孤立且無法解析跳轉的空標籤。
   * 一般教學導覽、章節標題及語句過渡文字不要求逐句標註引用。
9. **簡報三層對應架構 (Slide ➔ Wiki ➔ Raw Source)**：
   * 產出的 8～10 頁互動 HTML 簡報，每一頁核心知識點皆必須提供對應的 Wiki 條目連結，並能向上追溯至 Raw Source。
   * 所有在 GitHub Pages 上的跳轉錨點與外部連結必須真實可點擊。
10. **真實紀錄主義 (Empirical & Authentic Logging)**：
    * 嚴格禁止偽造紀錄或美化日誌。
    * 只記錄真實執行的指令、檢驗中實際浮現的錯誤、具體修改前後的 Diff，以及重測結果。

---

## 核心操作規範 (Operational Protocols)

### 1. Ingest 操作 (文獻攝取流程)
* **Step 1: 來源驗證**：檢查目標文獻的機構公信力、有效 URL，整理「中繼資料＋關鍵必要引述＋客觀摘要」存入 `raw/src-XX-<slug>.md`。
* **Step 2: 知識抽取**：提取文獻中的肢體信號、行為機制、情境因素，對照既有 Wiki 頁面。
* **Step 3: 條目建立/更新**：
  * 更新或建立 `wiki/entities/`（部位信號，如 `tail.md`、`eyes.md`）。
  * 更新或建立 `wiki/concepts/`（行為學概念，如 `calming-signals.md`、`ladder-of-aggression.md`）。
  * 更新或建立 `wiki/context/`（情境與迷思，如 `context-matters.md`、`myths-and-misconceptions.md`）。
  * 所有實質性行為學知識、定義、判斷與研究結果均須精準標記 `[^src-XX]`，並於文末提供完整腳註定義與檔案鏈結。一般教學導覽與過渡語句不強制逐句標記。
* **Step 4: 交叉索引更新**：在 `wiki/index.md` 中登記新條目或更新單行摘要與來源計數。
* **Step 5: 日誌追加**：在 `wiki/log.md` 以 `## [YYYY-MM-DD HH:MM] ingest | <Title>` 格式記錄攝取歷程。
* **Checkpoint A (攝取驗收)**：驗證新條目是否具備有效腳註且無空泛斷言。若未達標，依「最多修復 2 次」原則處置。

### 2. Query 操作 (知識查詢流程)
* **Step 1: 目錄檢索**：閱讀 `wiki/index.md` 定位相關條目。
* **Step 2: 綜合分析**：讀取目標頁面，比對跨條目觀點與情境條件。
* **Step 3: 產出回答**：產出初學者易懂之解答，文末明確列出 Wiki 參考條目與文獻出處。
* **備註**：若使用者希望將高品質回答沉澱為新條目，須獲明確指令後始得以「新綜合條目」寫入 `wiki/` 並更新 `index.md` 與 `log.md`。

### 3. Lint 操作 (健康檢查與一致性維護)
* **Layer 1: 程式結構檢查 (`scripts/check_links.py`)**：
  * 檢查所有 Markdown 內部鏈結（格式 `[[path/file]]` 或 `[text](path/file.md)`）是否均存在對應實體檔案。
  * 檢查是否存在無任何反向鏈結的「孤立條目 (Orphan Pages)」。
  * 檢查是否所有 Wiki 內頁皆出現在 `wiki/index.md` 中。
  * 檢查每篇 Wiki 條目是否至少包含一個 `[^src-xx]` 標註。
* **Layer 2: LLM 語意檢查**：
  * 抽查各條目陳述是否被標註的來源直接支持。
  * 檢查是否違反「非絕對化解讀」準則（如發現「搖尾巴即開心」應強制標註違規）。
  * 檢查不同來源間的合理差異是否被客觀保留，禁止為消除衝突而擅自扭曲文獻原意。
* **Checkpoint B (Lint 驗收)**：若檢查失敗，啟動修復流程（上限 2 次）；修復必須將【錯誤原因、修改 Diff、重新驗證結果】如實記入 `wiki/log.md`。

### 4. Build 操作 (互動式 HTML 簡報編譯)
* **簡報規模**：8～10 頁，以初學者視角編寫，語言生動生動但知識點嚴肅精確。
* **必備元素**：
  * 每頁明確標註來源溯源鏈（`Slide ➔ Wiki ➔ Raw Source`）。
  * 包含「破除常見迷思」、「安定訊號辨識」、「犬類攻擊階梯理論」、「綜合全身情境判讀」。
  * 包含 1～2 題互動式情緒判讀測驗（即時點擊反饋正確解析與文獻依據）。
* **Checkpoint C (發布驗收)**：
  * 驗證編譯後的 `docs/index.html` 語法無誤，能在本機與 GitHub Pages 零依賴正常渲染。
  * 抽驗簡報中的來源按鈕跳轉是否正常。

---

## 錯誤處理與熔斷升級規範 (Circuit Breaker & Escalation)

若在執行任何 Checkpoint 時未通過：
```text
[偵測到錯誤] 
   └── 紀錄錯誤細節至 wiki/log.md
   └── 第 1 次修復 ──> 重新檢驗
           └── 通過: 紀錄修正 Diff 與 PASS，繼續後續流程
           └── 未通過 ──> 第 2 次修復 ──> 重新檢驗
                   └── 通過: 紀錄修正 Diff 與 PASS，繼續後續流程
                   └── 未通過 ──> 【熔斷中斷】: 
                           1. 停止一切自動寫入
                           2. 在 wiki/log.md 標記 [ESCALATED_HITL]
                           3. 整理失敗摘要與原因，主動向使用者請求人工決策
```

---

## 檔案命名與格式規範

* **檔案命名**：一律使用小寫英數字與連字號（`kebab-case.md`）。
* **目錄結構維護**：
  * `raw/src-XX-<slug>.md`
  * `wiki/entities/<slug>.md`
  * `wiki/concepts/<slug>.md`
  * `wiki/context/<slug>.md`
* **文獻引用標籤**：`[^src-01]`、`[^src-02]` ... 須與 `raw/src-XX-...` 編號完全一致。
