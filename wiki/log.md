# 狗狗行為解密 LLM Wiki — 時間軸日誌 (log.md)

本文件為 Append-only（僅限追加）的系統日誌。所有 Ingest 攝取、Query 綜合、Lint 健康檢查及 Build 發布操作，均須嚴格按時間順序追加於文末。日誌標題格式統一為：
`## [YYYY-MM-DD HH:MM] operation | <簡短說明>`

---

## [2026-11-19 16:46] init | 專案初始化與規範建立
* **操作類型**：系統初始化 (Initialization)
* **執行動作**：
  1. 建立根目錄規範檔案 `AGENTS.md`，完整定義十項核心原則、操作工作流、重試熔斷與三層溯源標準。
  2. 初始化 `wiki/index.md` 內容導覽目錄結構。
  3. 初始化 `wiki/log.md` 時間軸日誌檔。
  4. 確認 `raw/` 原始資料夾已準備就緒，專案已建立 Git 版本控制。
* **狀態**：PASS（基礎架構建立完成，待進行資料文獻收集與 Ingest）

## [2026-11-19 16:55] audit | 原始文獻品質審查與版本替換 (Source Quality Audit & Replacement)
* **操作類型**：文獻品質與合規性審查 (Audit & Remediation)
* **審查發現與修正紀錄**：
  1. `src-01` (ASPCApro)：修正失效網址，更新為正式有效之 `https://www.aspcapro.org/resource/canine-body-language-tips`。
  2. `src-03` (VCA)：因 VCA 條款限制 AI 改作與再發布，原檔標記為 `deprecated_superseded`（保留作為審計歷程），正式替換為英國最大獸醫慈善機構 PDSA 之權威公開衛教指引 `raw/src-03-pdsa-prevent-stress-in-dogs.md`。
  3. `src-04` (Dogs Trust)：核對正文框架，修正概念定義——Dogs Trust 原始框架為「Whispering vs. Shouting（微小耳語至劇烈吶喊）」之溝通升級光譜，嚴格區隔 Kendal Shepherd (2004) 正式命名之階梯理論，避免概念混淆。
  4. `src-05` (AAHA)：核對正式文獻篇名《2015 AAHA Canine and Feline Behavior Management Guidelines》與官方網址，精準對齊指引中 Table 1 臨床焦慮與壓力指標。
  5. 著作權與授權查驗：全部 5 篇文獻均通過非商業課堂教學之合理使用與授權合規性審查。
* **狀態**：PASS（5 篇獨立有效文獻完成合規審查與版本替換）

## [2026-11-19 16:59] ingest | src-01: ASPCApro Canine Body Language Tips
* **操作類型**：文獻攝取 (Ingest)
* **新增/更新條目**：
  - `wiki/entities/eyes.md`
  - `wiki/entities/mouth.md`
  - `wiki/entities/tail.md`
  - `wiki/entities/ears.md`
  - `wiki/entities/posture.md`
  - `wiki/context/context-matters.md`
  - `wiki/context/myths-and-misconceptions.md`
* **整合重點**：建立各部位微表情基準，破除搖尾巴與打哈欠單一解讀迷思，確立全犬與情境評估法則。
* **狀態**：PASS（Checkpoint A 檢核通過：所有實質宣稱均具備有效 `[^src-01]` 腳註定義）

## [2026-11-19 17:00] ingest | src-02: RSPCA Understanding Dog Behaviour
* **操作類型**：文獻攝取 (Ingest)
* **新增/更新條目**：
  - 更新 `wiki/entities/posture.md`（抬前爪、炸毛立毛反應、邀玩鞠躬）
  - 更新 `wiki/entities/mouth.md`（鼻紋緊縮、露齒低吼、長唇對比）
  - 更新 `wiki/entities/eyes.md`（死盯警告、避視拉開距離）
  - 新增 `wiki/concepts/calming-signals.md`（拉開距離訊號與自我安撫機制）
  - 更新 `wiki/context/context-matters.md`（個體基準線、突變優先排除生理疾病與疼痛）
* **交叉比對重點**：將 ASPCApro 的各部位微信號，與 RSPCA 的「拉開距離 vs 拉近距離」社交功能分類進行整合。
* **狀態**：PASS（Checkpoint A 檢核通過：所有實質宣稱均具備有效 `[^src-02]` 腳註定義）

## [2026-11-19 17:01] ingest | src-03: PDSA Tips to Identify and Prevent Stress in Dogs
* **操作類型**：文獻攝取 (Ingest)
* **新增/更新條目**：
  - 更新 `wiki/entities/ears.md`（緊繃貼耳與恐懼指標）
  - 更新 `wiki/entities/tail.md`（低垂與夾尾之安全感喪失指標）
  - 更新 `wiki/context/myths-and-misconceptions.md`（新增迷思三：嚴禁懲罰壓力行為）
  - 新增 `wiki/concepts/displacement-behavior.md`（轉移行為成因、嗅聞舔鼻與安全避風港原則）
* **合規性檢核**：嚴格使用 `raw/src-03-pdsa-prevent-stress-in-dogs.md`，零引用已封存之 VCA 檔案。
* **狀態**：PASS（Checkpoint A 檢核通過：所有實質宣稱均具備有效 `[^src-03]` 腳註定義）

## [2026-11-19 17:02] ingest | src-04: Dogs Trust Dog Body Language & Communication
* **操作類型**：文獻攝取 (Ingest)
* **新增/更新條目**：
  - 新增 `wiki/concepts/communication-escalation.md`（耳語到吶喊模型、經驗學習跳級咬傷機制、與攻擊階梯之學術對齊）
  - 新增 `wiki/concepts/trigger-stacking.md`（壓力誘發物堆疊效應、皮質醇累積與閾值突破）
  - 更新 `wiki/context/myths-and-misconceptions.md`（新增迷思四：低吼是警報器，嚴禁懲罰以防拆除警報器效應）
* **概念精確度檢核**：嚴格依 Dogs Trust 原文定義「耳語 vs. 吶喊」，並標註其與 Kendal Shepherd 階梯理論之對照，不生搬硬套。
* **狀態**：PASS（Checkpoint A 檢核通過：所有實質宣稱均具備有效 `[^src-04]` 腳註定義）

## [2026-11-19 17:03] ingest | src-05: 2015 AAHA Canine Behavior Management Guidelines
* **操作類型**：文獻攝取 (Ingest)
* **新增/更新條目**：
  - 新增 `wiki/concepts/fas-spectrum.md`（FAS 光譜、Table 1 焦慮臨床指標、凍結定格 vs 躁動徘徊極端光譜）
  - 更新 `wiki/entities/posture.md`（定格凍結 Freezing 行為學意義、被動順從之危險誤解）
  - 更新 `wiki/entities/eyes.md`（散瞳 Mydriasis、環境過度掃視 Hypervigilance、社交抽離）
  - 更新 `wiki/entities/mouth.md`（臉部鬼臉 Facial Grimace、自律神經流涎徵象）
  - 更新 `wiki/context/myths-and-misconceptions.md`（新增迷思五：凍結定格不代表溫馴，實為高危險臨界點）
* **整合重點**：引入獸醫臨床醫學層次之客觀生理指標（Table 1），為大眾行為觀察提供堅實之神經生物學支持。
* **狀態**：PASS（Checkpoint A 檢核通過：所有實質宣稱均具備有效 `[^src-05]` 腳註定義）

## [2026-11-19 17:04] checkpoint | Checkpoint A: 全五篇 Ingest 成果彙總與驗收
* **操作類型**：檢查節點 A 驗收 (Ingest Checkpoint Validation)
* **檢核項目**：
  1. 來源腳註解析度：12 個 Wiki 知識條目中，所有 `[^src-xx]` 標註均於頁尾具備對應之實體 `raw/` 檔案超連結與文獻出處，無任何孤立未解析標籤。
  2. 宣稱溯源性：所有重要行為學定義與機制均嚴格溯源，未有憑空捏造之斷言。
  3. 非絕對化原則：嚴格落實四大維度（全身、環境、情境、基準線），杜絕「搖尾巴即開心」等單一化誤判。
  4. VCA 封存隔離：全 Wiki 條目零引用 `src-03-vca`，`src-03` 全面採納 PDSA 權威指引。
  5. 條目冗餘度：無同義重複條目，實體（部位）、機制（概念）、情境（迷思）三層結構分明。
* **驗收結果**：PASS（零重試，一次性通過驗收標準）

## [2026-11-20 15:50] query | 唯讀查詢檢索實測 (Read-Only Query Verification)
* **操作類型**：知識查詢 (Query)
* **檢索題目**：
  1. 狗狗搖尾巴一定代表開心嗎？（命中：`wiki/entities/tail.md`, `wiki/context/myths-and-misconceptions.md`）
  2. 狗狗打哈欠、舔嘴唇是否一定代表緊張？（命中：`wiki/entities/mouth.md`, `wiki/concepts/calming-signals.md`, `wiki/context/context-matters.md`）
  3. 狗狗突然僵住不動代表什麼？主人如何安全回應？（命中：`wiki/entities/posture.md`, `wiki/concepts/communication-escalation.md`, `wiki/concepts/fas-spectrum.md`, `wiki/context/myths-and-misconceptions.md`）
* **原則確認**：全程採唯讀模式檢索，Wiki 知識庫未發生任何寫入或變更。

## [2026-11-20 15:51] lint | 程式結構檢驗與 LLM 語意審查 (Dual-Layer Linting)
* **操作類型**：雙層健康檢查 (Dual-Layer Lint)
* **Layer 1: 程式結構檢查 (`scripts/check_links.py`)**：
  - 檢核範圍：12 篇正式 Wiki 內容頁、5 篇有效原始資料中繼檔。
  - 檢核項目：內部鏈結有效性、索引目錄登記、孤立條目偵測、來源腳註閉合、已封存 VCA 隔離。
  - 檢核輸出：0 斷鏈、0 孤立頁、0 未定義腳註、0 違規引用。
  - 結果：**PASS（程式檢查合格）**
* **Layer 2: LLM 語意審查 (Semantic Review)**：
  - 抽查項目：
    1. 尾巴擺動高度/僵硬度與攻擊警戒關聯（對應 `src-01` Anchor-01-D）。
    2. 打哈欠/舔唇作為拉開距離訊號（對應 `src-02` Anchor-02-A）。
    3. 嚴禁懲罰焦慮破壞行為（對應 `src-03` Anchor-03-C）。
    4. 處罰低吼等同拆除警報器（對應 `src-04` Anchor-04-B）。
    5. 定格凍結為高危險臨界點非溫馴（對應 `src-05` Anchor-05-B）。
  - 結果：**PASS（語意審查合格，5 項核心宣稱 100% 獲原始來源真實支持，無絕對化斷言）**

## [2026-11-20 15:52] loop-test | 閉環容錯與修復熔斷實測 (Fault-Injection Loop Test)
* **操作類型**：Graph 閉環容錯機制驗證 (Fault Injection Test)
* **說明**：本測試為**人工注入的測試錯誤**，在隔離副本 `wiki_fault_test/` 中執行，正式 Wiki 未受污染。
* **測試流程**：
  1. 建立測試環境：複製 `wiki/` 至 `wiki_fault_test/`。
  2. 人工注入錯誤：在 `wiki_fault_test/entities/eyes.md` 將 `[[wiki/entities/mouth|犬隻嘴部與臉部張力]]` 改為不存在之 `[[wiki/entities/non-existent-snout|犬隻口鼻錯誤連結]]`。
  3. 執行檢驗：`scripts/check_links.py` 成功攔截並報錯 `[FAIL] Broken internal wikilink: '[[wiki/entities/non-existent-snout...]]'`。
  4. 執行修復 (第 1 次重試修復)：復原為正確之 `mouth.md` 鏈結。
  5. 重新檢驗：`scripts/check_links.py` 輸出 `[PASS]`。
  6. 清理測試環境：安全移除 `wiki_fault_test/`。
* **驗收結果**：PASS（閉環偵錯與自動修復機制運作正常，重試 1 次即修復，未觸發 2 次熔斷）
