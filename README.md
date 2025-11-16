# specDevAgent — GitHub 專案說明文件

## 📘 專案簡介
**specDevAgent** 是一個標準化的 AI 代理開發規範模板，源自 *dev-agent-spec* 專案，旨在協助開發者快速建立、管理與維運 AI 代理人（Agent）驅動的軟體開發流程。

透過文件導向與任務循環設計，代理人可以：
- 自動建立專案骨架與文件
- 追蹤任務進度與提交紀錄
- 依規範完成開發、測試與文件更新

---

## 🚀 快速開始
```bash
# 1. 建議使用虛擬環境（可選）
python -m venv .venv && source .venv/bin/activate

# 2. 查看 CLI 使用說明與可用子命令
python cli/agent_cli.py --help

# 3. 初始化專案骨架（可加上 --force 重新產生）
python cli/agent_cli.py init ./example-project

# 4. 匯入樣板（目前提供 python-fastapi，必要時可加 --force）
python cli/agent_cli.py scaffold ./example-project --template python-fastapi

# 5. 驗證專案結構與中繼資料
python cli/agent_cli.py validate ./example-project

# 6. 針對 project.json 執行靜態檢查（可加 --check-documents）
python cli/agent_cli.py lint-metadata ./example-project --check-documents
```

> 💡 `init` 會建立 `project.json`、基礎文件與目錄結構；`scaffold` 會將樣板程式碼複製到指定資料夾；`validate` 檢查整體結構是否符合規範；`lint-metadata` 則專注於 `project.json` 的欄位格式、角色枚舉與文件路徑引用，適合在提交前快速檢查。

### `project.json` 範例

初始化後請依實際專案更新 `project.json`。下方範例展示所有必填欄位與常見的代理人定義：

```json
{
  "name": "Document Scanner MVP",
  "description": "Pipeline for extracting structured data from PDFs",
  "version": "0.1.0",
  "agents": [
    {
      "id": "orchestrator-bot",
      "role": "orchestrator",
      "responsibilities": [
        "Refine backlog items",
        "Coordinate development log updates"
      ]
    },
    {
      "id": "builder-bot",
      "role": "developer",
      "responsibilities": [
        "Deliver FastAPI endpoints",
        "Maintain unit tests"
      ]
    }
  ],
  "documents": {
    "project": "project.md",
    "todo": "todo.md",
    "log": "development.log"
  }
}
```

### Metadata 靜態檢查指引

- 執行 `python cli/agent_cli.py lint-metadata <project-path>` 可單獨檢查 `project.json`，使用 `--check-documents` 時會確認 `project.md`、`todo.md`、`development.log` 等路徑是否存在。
- `agents[].id` 必須為 kebab-case（例：`orchestrator-bot`），`agents[].role` 則須為 `developer`、`orchestrator`、`qa`、`researcher` 或 `reviewer` 之一。
- `name`、`description` 與 `responsibilities` 皆需為非空字串，`documents.project` / `documents.todo` 需指向 `.md` 檔案。

### 代理人互動範例流程

```text
使用者：我要建立一個文件掃描系統，請按照規範建立 MVP。

代理人：
1. 執行 `python cli/agent_cli.py init ./document-scanner` 建立骨架。
2. 依需求更新 `project.json` 與 `todo.md`。
3. 執行 `python cli/agent_cli.py scaffold ./document-scanner --template python-fastapi` 匯入 API 範本。
4. 補上樣板所需環境：`python -m pip install -r ./document-scanner/requirements.txt`。
5. 驗證結構：`python cli/agent_cli.py validate ./document-scanner`。
6. 執行 `python cli/agent_cli.py lint-metadata ./document-scanner --check-documents`，確保 `project.json` 維持可讀性與一致性。
7. 執行 `pytest` 確認樣板測試通過並於 `development.log` 記錄。

使用者：下一步請完成 T002。

代理人：查閱 `todo.md` 及 `development.log`，依照任務循環繼續實作。
```

---

## 📂 主要資料夾結構
```
specDevAgent/
├─ agent.md                ← 代理人主要規範文件
├─ templates/              ← 語言樣板（目前提供 Python FastAPI）
├─ schema/                 ← JSON Schema 格式驗證
├─ cli/                    ← CLI 工具（init / validate / scaffold）
├─ docs/                   ← 說明文件與工作流程
│  ├─ overview.md
│  └─ bootstrap-workflow.md
└─ LICENSE
```

---

## 💡 功能亮點
- **任務循環（PLAN → CHANGES → TEST → GIT → LOG → DoD）**：確保每個任務皆可追蹤與驗證。
- **文件驅動開發**：以 `project.md`, `todo.md`, `development.log` 為核心文件，確保 AI 能讀懂專案上下文。
- **樣板支援**：提供 Python FastAPI 的最小可運行樣板（含應用程式與測試）。
- **Metadata 靜態分析**：`lint-metadata` 子命令確保 `project.json` 符合 JSON Schema 與角色/ID 規範，並可選擇檢查文件路徑是否存在。
- **CI / PR 標準整合**：可依專案需求擴充 Conventional Commits、PR 驗收檢查與自動驗證。

---

## 🧠 使用情境範例
### 建立新專案（代理人協助流程）
1. 你在 VS Code 中輸入：
   ```
   我要建立一個文件掃描系統，請幫我依規範建立 MVP。
   ```
2. 代理人會自動：
   - 產生 `docs/discovery.md`、`docs/inception.md`
   - 建立 `project.md`, `todo.md`, `development.log`
   - 建立初始端點與單測
3. 你可說：「下一步請完成 T002」，代理人會自動查 `todo.md` 並繼續任務循環。

---

## 🧩 開發原則
| 類別 | 原則 |
|------|------|
| 可追溯性 | 每個任務均需在 `development.log` 留痕 |
| 文件一致性 | 所有開發變更須更新文件 |
| 測試完整性 | 每個端點必須有最小測試 |
| 安全控管 | 所有敏感資訊透過 `.env` 管理 |
| 可擴充性 | 支援接入 RAG、MCP 或外部 API 工具 |

---

## 🔭 下一步行動與改善建議
最新的改進路線圖會持續整理在 [`docs/next-steps.md`](docs/next-steps.md)。重點工作流摘要如下：

1. **CLI 回歸測試自動化（P0）**：以 pytest 操控 `cli/agent_cli.py`，確保 `init / scaffold / validate` 指令在 CI 中全數跑過並維持 3 分鐘內完成。
2. **樣板套件化（P1）**：將 FastAPI 樣板拆成可版本化的套件，並允許 CLI 透過 `--template python-fastapi@x.y.z` 取得可重複的 scaffold。
3. **代理人手冊與範例（P1）**：為文件新增完整情境對話與錯誤排除範例，並在 CLI `--help` 中加註相關章節方便查閱。
4. **Metadata 靜態分析（P2）**：擴充 `project.schema.json`、提供 `lint-metadata` 子命令與 pre-commit 勾點，確保 `project.json` 長期維持高品質。

想確認目前狀態、負責團隊或退出條件，可直接檢視該文件頂端的儀表板表格。

---

## 🧾 授權與貢獻
本專案採用 **MIT License**。
歡迎以 Pull Request 或 Issue 的方式貢獻新範本、改進 CLI 工具、或新增語言樣板。

---

## 📎 GitHub 專案徽章建議
可於 README 首段加入：
```
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)
```

---

## 📧 聯絡與引用
開發者：**dof（劉瑞弘）** ｜ National Chin-Yi University of Technology  
專案首頁：[https://github.com/dofliu/specDevAgent](https://github.com/dofliu/specDevAgent)

---

© 2025 specDevAgent — AI Agent-Oriented Development Framework
