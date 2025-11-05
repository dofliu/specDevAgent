# specDevAgent 概觀

specDevAgent 為 AI 協助軟體開發而設計的標準化模板。它結合 CLI 工具、
JSON Schema 與文件規範，讓代理人能夠在一致的結構下啟動、驗證與擴充專案。

## 核心元件
- **CLI (`cli/agent_cli.py`)**：提供 `init`、`validate`、`scaffold` 三種指令。
  - `init`：生成必要目錄與文件，包含 `project.json` 中的專案中繼資料。
  - `validate`：檢查專案是否符合目錄結構與中繼資料規範。
  - `scaffold`：將指定樣板（如 `python-fastapi`）套用到目標資料夾。
- **文件集合**：以 `project.md`、`todo.md`、`development.log` 為核心，
  並輔以 Discovery、Inception、ADR 等文件確保上下文完整。
- **樣板資料夾**：提供可立即運行的程式碼骨架，降低代理人搭建環境的成本。
- **Schema (`schema/project.schema.json`)**：定義專案中繼資料欄位，確保代理人能
  以一致的方式讀取與更新專案狀態。

## 代理人協作流程
1. 讀取核心文件掌握需求與任務狀態。
2. 透過 CLI 建立或驗證專案骨架。
3. 根據任務使用樣板快速導入必要的程式與測試。
4. 執行測試並更新 `development.log` 與 `todo.md`。
5. 以 PR 匯報並等待人工審核。

此流程強調文件與程式碼並重，確保 AI 代理在多次迭代後仍能維持高可靠度。
