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
