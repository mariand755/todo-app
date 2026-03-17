# Todo-App
A Docker-first To-Do app with a Python FastAPI backend (plus CLI/library) and a React frontend, supporting folder/item CRUD and ordering, with CI-enforced quality and health checks.

**Contents overview:**
- `backend/`:
   - Python backend and command-line interface.
   - CLI entry: `backend/commandline_interface/main.py`.
   - Core library lives in `backend/library/`.

- `frontend/`:
   - React app (development with `npm run dev`).


## Features
- **Backend (Python)**:
   CLI entry `backend/commandline_interface/main.py`, core library in `backend/library/` (folder & item management).

- **Frontend (React)**:
   Single-page app in `frontend/` for a graphical UI.

- **Folder Management**:
   Add, edit, delete, and pin/unpin folders; search by title; list folders. Pinned folders sort to the top of the sidebar.

- **Todo Item Management**: Add, edit, delete, toggle completion, and reorder items within folders; search by title; list items.

- **Persistence**:
   SQLAlchemy models backed by Postgres (env-driven) with SQLite fallback; soft deletes via `is_deleted` flags; `is_pinned` column on folders.

- **User-Friendly CLI**:
   Interactive prompts and command aliases for quick navigation.

- **Dev & Deployment**:
   Dockerfiles for `backend` and `frontend`; `docker-compose.yaml` to run services locally with health checks.

- **Testing**:
   Backend: unit tests (`BUT##` markers) and integration tests (`BINT##` markers) under `backend/tests/`.
   Frontend: unit tests (`@FUT## |` Vitest title prefixes) and integration tests (`@FINT## |` Vitest title prefixes) under `frontend/src/test/`.


## Project Structure
Note: Dotfiles and dotfolders (.*) omitted
```
todo-app/
├── docker-compose.yaml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── app/
│   │   ├── api.py
│   │   └── logging_config.py
│   ├── commandline_interface/
│   │   └── main.py
│   ├── db/
│   │   └── db_setup.sql
│   ├── library/
│   │   ├── folder_manager.py
│   │   ├── folder.py
│   │   ├── models.py
│   │   └── todo_item.py
│   └── tests/
│       ├── conftest.py
│       ├── helpers.py
│       ├── integration/
│       │   ├── test_api.py
│       │   ├── test_item_order_persistence.py
│       │   └── test_positions_integration.py
│       └── unit/
│           ├── test_folder.py
│           ├── test_folder_manager.py
│           ├── test_folder_positions.py
│           ├── test_models.py
│           ├── test_position_mapping.py
│           └── test_positions.py
├── docs/
│   ├── ci-governance.md
│   └── frontend-docker.md
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── logger.js
│       ├── main.jsx
│       ├── useApi.js
│       ├── components/
│       │   ├── FolderItem.jsx
│       │   ├── LandingContent.jsx
│       │   ├── LoadingContent.jsx
│       │   ├── MainContent.jsx
│       │   ├── NewFolderForm.jsx
│       │   ├── Sidebar.jsx
│       │   └── TodoItem.jsx
│       └── test/
│           ├── integration/
│           │   └── App.integration.test.jsx
│           └── unit/
│               ├── api/
│               │   └── useApi.unit.test.js
│               └── components/
│                   ├── FolderItem.test.jsx
│                   ├── LandingContent.test.jsx
│                   ├── LoadingContent.test.jsx
│                   ├── MainContent.test.jsx
│                   ├── NewFolderForm.test.jsx
│                   ├── Sidebar.test.jsx
│                   └── TodoItem.test.jsx
└── scripts/
   ├── fix_frontend_it_callbacks.py
   ├── rewrite_frontend_test_ids.py
   ├── rewrite_test_id_markers.py
   └── terminal_command.sh
```


## Getting Started

### Prerequisites
- Python `3.11` or higher (recommended)
- Node.js `16+` and npm (for the frontend)

### Installation
Clone the repository:
```sh
git clone git@github.com:mariand755/todo-app.git
cd todo-app
```

### Running the App
Run the CLI (backend):
```sh
python backend/commandline_interface/main.py
```

Run the frontend (development):
```sh
cd frontend
npm install
npm run dev
```

Or run the full stack with Docker Compose (if configured):
```sh
docker compose up --build --wait
```

- Full reset if local state gets stuck (destructive): `docker compose down -v && docker compose up -d --build --wait`

## QA & CI Commands

### Backend (Docker-first)

Build backend test image:
```sh
docker build -f backend/Dockerfile --target test -t todo-app-backend-test ./backend
```

Run all backend tests:
```sh
docker run --rm todo-app-backend-test uv run pytest -q -o addopts=''
```

Run backend slices:
```sh
docker run --rm todo-app-backend-test uv run pytest -q -o addopts='' -m integration
docker run --rm todo-app-backend-test uv run pytest -q -o addopts='' -m unit
```

### Frontend (Docker-first)

Build frontend test image:
```sh
docker build -f frontend/Dockerfile -t todo-app-frontend-test ./frontend
```

Run all frontend tests:
```sh
docker run --rm todo-app-frontend-test npm run test
```

Run frontend slices:
```sh
docker run --rm todo-app-frontend-test npm run test -- --run src/test/integration
docker run --rm todo-app-frontend-test npm run test -- --run src/test/unit
```

### Test ID Notes

- Canonical testing policy: docs/testing-governance.md
- Backend test IDs use pytest markers and can be selected with -m.
- Frontend test IDs use Vitest title prefixes and can be selected with -t.

### CI Workflows

- Backend Docker CI: `.github/workflows/docker_backend.yml`
- Frontend Docker CI: `.github/workflows/docker_frontend.yml`
- Compose Health CI: `.github/workflows/compose_health.yml`

### CI Governance and Docs

- CI policy (triage, SLOs, flaky cleanup): `docs/ci-governance.md`
- Frontend Docker guide: `docs/frontend-docker.md`

## Features Overview
- Follow the interactive prompts to manage folders and todo items from the CLI.
- Or use the React frontend for a graphical experience.

### Usage
- **Folders:**
   - Add, view, edit, delete, pin/unpin, and search folders via the CLI or the frontend UI.
   - Pinned folders always sort to the top of the sidebar.

- **Items:**
   - Add, view, edit, delete, toggle completion, and reorder todo items inside a selected folder.

- **Exit:**
   - Quit the CLI with the `exit` command
   - Or close the frontend browser tab.


### Example Workflow
1. Start the CLI:
   ```sh
   python backend/commandline_interface/main.py
   ```
2. Add a folder:
   - Choose `folders` → `add` in the CLI
   - Or use the frontend New Folder form.

3. Add items to a folder:
   - Choose `items` → select folder ID → `add`.

4. Edit or delete items/folders:
   - Use the `edit` / `delete` commands in the CLI
   - Or the frontend controls.

5. Exit the CLI:
   - Enter `exit`
   - Or stop `docker compose` / close the frontend tab.


---

**Author:**
Marian Dadzie
