# MCK Church App — Dev Environment Setup (Kali Linux + VS Code)

Everything needed on top of Docker to work on this project comfortably:
backend (Django), admin panel (Vue), mobile (Flutter — not containerized).

---

## 1. System software (install on Kali, outside containers)

You still need these on the host even though the app itself runs in Docker,
because VS Code, Flutter, and linting/tooling need them locally.

| Tool | Why |
|---|---|
| Docker Engine + Compose plugin | runs all the containers |
| Git | version control |
| Python 3.12 + venv | local linting/autocomplete for Pylance, running one-off scripts |
| Node.js 20 (via nvm) | Vue admin tooling outside Docker if you want faster HMR, and for `npm` CLI use |
| Flutter SDK + Dart | mobile app — not containerized, run natively |
| Android SDK cmdline-tools + Java 17 (Temurin) | required by Flutter to build/run Android |
| PostgreSQL client (`psql`) | inspect the DB directly without shelling into the container |
| Redis CLI (`redis-tools`) | inspect cache/broker directly |
| httpie or Postman/Insomnia | testing API endpoints |
| VS Code | editor |

### 1.1 Docker Engine + Compose

Kali's default `docker.io` package is often outdated — use Docker's official repo:

```bash
# remove old versions if present
sudo apt remove docker docker-engine docker.io containerd runc

# set up Docker's apt repo (Debian-based, works on Kali)
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian bookworm stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# run docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# verify
docker --version
docker compose version
```

### 1.2 Git

```bash
sudo apt install -y git
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 1.3 Python 3.12 + venv (for local tooling, not for running the app — that's Docker's job)

```bash
sudo apt install -y python3 python3-venv python3-pip
python3 --version   # confirm 3.11+ (Kali usually ships recent Python)

# create a local venv just so VS Code/Pylance can resolve imports for autocomplete
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 1.4 Node.js via nvm (for the Vue admin panel)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
node --version
npm --version
```

### 1.5 Flutter SDK + Android tooling

```bash
# Java 17 (Temurin) — required by Android Gradle builds
sudo apt install -y wget apt-transport-https gnupg
wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo apt-key add -
echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | \
  sudo tee /etc/apt/sources.list.d/adoptium.list
sudo apt update
sudo apt install -y temurin-17-jdk

# Flutter SDK
sudo apt install -y curl git unzip xz-utils zip libglu1-mesa
cd ~
git clone https://github.com/flutter/flutter.git -b stable
echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
source ~/.bashrc

flutter doctor    # follow its prompts (Android licenses, missing tools, etc.)

# Android SDK cmdline-tools (flutter doctor will point you to install these
# via Android Studio, or headlessly via sdkmanager if you skip Android Studio)
flutter doctor --android-licenses
```

If you don't need to build/test on a physical Android device or emulator
day-to-day, `flutter doctor` warnings about Android Studio can be ignored
until you do — `flutter run -d chrome` (web) or `flutter test` still work
without full Android tooling.

### 1.6 PostgreSQL + Redis CLI clients

```bash
sudo apt install -y postgresql-client redis-tools

# once containers are up:
psql -h localhost -p 5432 -U mck_user -d mck_church
redis-cli -h localhost -p 6379 ping
```

### 1.7 API testing tool

```bash
sudo apt install -y httpie
# or install Insomnia / Postman as a .deb / AppImage if you prefer a GUI
```

### 1.8 VS Code

```bash
sudo apt install -y wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | \
  sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
rm packages.microsoft.gpg
sudo apt update
sudo apt install -y code
```

---

## 2. VS Code extensions

Install all at once from the project root once `.vscode/extensions.json`
(included in this drop) is in place — VS Code will prompt "install
recommended extensions." Or install manually:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension batisteo.vscode-django
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-vscode-remote.remote-containers
code --install-extension redhat.vscode-yaml
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension Vue.volar
code --install-extension Dart-Code.dart-code
code --install-extension Dart-Code.flutter
code --install-extension eamodio.gitlens
code --install-extension mikestead.dotenv
code --install-extension usernamehw.errorlens
code --install-extension gruntfuggly.todo-tree
code --install-extension editorconfig.editorconfig
code --install-extension humao.rest-client
code --install-extension bradlc.vscode-tailwindcss
```

| Extension | Purpose |
|---|---|
| Python + Pylance | Django backend autocomplete, type checking |
| Django (batisteo) | template/model syntax highlighting, snippets |
| Docker | manage images/containers/compose from the sidebar |
| Dev Containers | optional — attach VS Code directly inside the `backend` container |
| YAML (redhat) | schema validation for `docker-compose.yml` |
| ESLint + Prettier | Vue admin panel linting/formatting |
| Volar | Vue 3 language support (replaces old Vetur) |
| Dart + Flutter | mobile app development, widget inspector, hot reload |
| GitLens | inline blame, history, branch comparison |
| DotENV | syntax highlighting for `.env` files |
| Error Lens | inline error/warning display |
| Todo Tree | surfaces `TODO`/`FIXME` across the whole repo — useful given this spec's "flagged for follow-up" notes |
| EditorConfig | keeps indentation/style consistent across Python/JS/Dart |
| REST Client | test API endpoints straight from `.http` files in-editor |
| Tailwind CSS IntelliSense | if the Vue admin panel uses Tailwind |

`.vscode/settings.json` (included) points Pylance at `backend/.venv`, turns
on format-on-save for Python/Vue/JS, and sets Prettier as the default
formatter for the admin panel.

---

## 3. Optional: Dev Containers (attach VS Code inside Docker)

Since the backend actually runs in a container, you can skip the local
venv entirely and develop *inside* the container instead — same Python
version, same installed packages, no host/container drift.

1. Install the **Dev Containers** extension (already listed above).
2. `docker compose up -d`
3. Command Palette → **Dev Containers: Attach to Running Container** → pick `mck_backend`.
4. VS Code reopens with a window running inside the container — install
   Python/Pylance extensions *inside* that window when prompted (VS Code
   asks separately for container-side extensions).

This is optional — the local venv approach in 1.3 works fine for
autocomplete-only use.