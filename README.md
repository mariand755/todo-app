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
   Add, edit, delete folders; search by title; list folders.

- **Todo Item Management**: Add, edit, delete items within folders; search by title; list items.

- **Persistence**:
   Simple SQL setup in `backend/db/db_setup.sql` for storing folders and items.

- **User-Friendly CLI**:
   Interactive prompts and command aliases for quick navigation.

- **Dev & Deployment**:
   Dockerfiles for `backend` and `frontend`; `docker-compose.yaml` to run services locally with health checks.

- **Testing**:
   Unit tests under `backend/tests/`.
   Integration tests under `backend/tests/`.


## Project Structure
Note: Dotfiles and dotfolders (.*) omitted
```
todo-app/
├── docker-compose.yaml
├── README.md
├── TO Do List
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   └── api.py
│   ├── commandline_interface/
│   │   └── main.py
│   ├── db/
│   │   └── db_setup.sql
│   ├── library/
│   │   ├── __init__.py
│   │   ├── folder_manager.py
│   │   ├── folder.py
│   │   ├── models.py
│   │   └── todo_item.py
│   └── tests/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── useApi.js
│       └── components/
│           ├── FolderItem.jsx
│           ├── LandingContent.jsx
│           ├── MainContent.jsx
│           ├── NewFolderForm.jsx
│           ├── Sidebar.jsx
│           └── TodoItem.jsx
└── scripts/
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
   - Add, view, edit, delete, and search folders via the CLI
   - Or the frontend UI.

- **Items:**
   - Add, view, edit, delete, and search todo items inside a selected folder.

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
