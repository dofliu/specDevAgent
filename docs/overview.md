# specDevAgent 概觀

specDevAgent 為 AI 協助軟體開發而設計的標準化模板。它結合 CLI 工具、
JSON Schema 與文件規範，讓代理人能夠在一致的結構下啟動、驗證與擴充專案。

## 核心元件
- **CLI (`cli/agent_cli.py`)**：提供 `init`、`validate`、`scaffold` 與 `lint-metadata` 指令。
  - `init`：生成必要目錄與文件，並建立含預設欄位的 `project.json`。
  - `validate`：檢查專案是否符合目錄結構、中繼資料以及文件引用規範。
  - `scaffold`：將指定樣板（如 `python-fastapi`）套用到目標資料夾，可使用 `--force` 覆寫既有檔案。
  - `lint-metadata`：針對 `project.json` 執行靜態分析，檢查名稱、描述、代理人 ID/角色與文件路徑設定。
- **文件集合**：以 `project.md`、`todo.md`、`development.log` 為核心，
  並輔以 Discovery、Inception、ADR 等文件確保上下文完整。
- **樣板資料夾**：提供可立即運行的程式碼骨架，降低代理人搭建環境的成本。
- **Schema (`schema/project.schema.json`)**：定義專案中繼資料欄位，確保代理人能
  以一致的方式讀取與更新專案狀態。

## 代理人協作流程
1. 讀取核心文件掌握需求與任務狀態。
2. 透過 CLI 建立或驗證專案骨架，並於 `project.json` 補上正確的名稱、描述與代理人資訊。
3. 根據任務使用樣板快速導入必要的程式與測試，確保 `requirements.txt` 依賴可被安裝。
4. 執行測試並更新 `development.log` 與 `todo.md`，同時檢查 `project.json` 中文件路徑皆指向存在的檔案。
5. 在提交前執行 `python cli/agent_cli.py lint-metadata <project-path> --check-documents`，確保 `project.json` 內容符合 JSON Schema 與路徑規範。
6. 以 PR 匯報並等待人工審核，PR 需附上測試指令與結果摘要。

## Metadata Linting 指南

1. **ID 與角色**：所有 `agents[].id` 須為 kebab-case（`builder-bot`），`agents[].role` 限制在 `developer`、`orchestrator`、`qa`、`researcher`、`reviewer` 清單內。
2. **文字欄位**：`name` 至少 3 個字元、`description` 至少 10 個字元；`responsibilities` 每個項目需為具體動詞敘述。
3. **文件路徑**：`documents.project` 與 `documents.todo` 必須指向 `.md` 檔案，`documents.log` 須存在於倉庫中且可透過 `--check-documents` 自動驗證。
4. **建議流程**：在 `validate` 前先執行 `lint-metadata`，可避免結構驗證因中繼資料錯誤而中斷。

此流程強調文件與程式碼並重，確保 AI 代理在多次迭代後仍能維持高可靠度。
