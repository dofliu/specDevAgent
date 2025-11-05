# Bootstrap 工作流程

以下流程協助代理人在全新環境中快速啟動專案並交付第一個增量。

## 1. 環境設定
1. 建立虛擬環境並安裝依賴（若使用樣板則依 `requirements.txt`）。
2. 取得專案倉庫與必要的 API/工具憑證。

## 2. 專案初始化
1. 執行 `python cli/agent_cli.py init <project-path>` 生成目錄結構（必要時以 `--force` 重置）。
2. 檢視 `project.json` 並填入專案實際資訊（名稱、描述、版本、代理人角色與文件路徑）。
3. 將 `docs/decisions/adr-0001.md` 更新為真實決策內容，並確認 `documents` 欄位指向存在的檔案。

## 3. 任務啟動
1. 依需求更新 `todo.md`，建立首批任務條目與狀態。
2. 於 `development.log` 開啟新區塊，記錄預計交付內容與測試策略。
3. 若需要範本程式碼，使用 `scaffold` 導入對應樣板（如 `python-fastapi`）。

## 4. 開發與驗證
1. 完成程式碼與文件變更後執行測試（`pytest`、`uvicorn` smoke test 等）。
2. 透過 `python cli/agent_cli.py validate <project-path>` 確認目錄、`project.json` 欄位與文件路徑皆符合規範。
3. 將測試結果與觀察寫入 `development.log`，並視需求更新 `project.json` 版本號或代理人責任。

## 5. 提交與交付
1. 使用 Conventional Commit 撰寫提交訊息並推送分支。
2. 建立 PR，摘要需包含變更重點與測試指令。
3. 在 PR 描述中附上對應的 `todo.md` 條目與狀態更新。

依循上述步驟可確保每位代理人都能以一致且可靠的方式啟動新專案。
