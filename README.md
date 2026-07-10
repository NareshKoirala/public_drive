# Local Cloud Data Pipeline (Private NAS)

A lightweight, secure, and self-hosted local cloud system built with **FastAPI** and **Python**. This system allows any device connected to your local Wi-Fi network (such as a mobile phone) to manage files on external storage drives attached to a host laptop or headless server without transmitting sensitive operating system credentials.

---

## 🚀 Features

* **Automated Storage Discovery:** Uses `lsblk` to scan and display only connected external partitions, dynamically extracting their size, name, and mount status.
* **Hybrid Mount Architecture:** Automatically utilizes existing desktop mount points (e.g., `/run/media/...`) or gracefully handles fallback passwordless mounting (e.g., `/mnt/[UUID]`) on headless systems.
* **Secure Network Isolation:** Separates web-layer authentication from host OS-layer permissions, preventing systemic exposure.
* **Robust Core Pipeline:** Exposes 4 distinct file operations: upload, download, folder creation, and targeted item deletion.
* **Path Traversal Prevention:** Hardcoded safety nets isolate file manipulations strictly within the boundaries of the active storage device root.

---

## 🛠️ System Architecture


```

[ PHONE UI ]
│
(1. Authenticates with Web Password)
│
▼
[ PYTHON WEB BACKEND ] ──(2. Runs lsblk -p -l -J)──► [ LINUX KERNEL ]
│                                                 │
◄──(3. Filters: type=='part' & name=='/dev/sd*')──┘
│
(4. Sends Clean Drive List to UI)
│
▼
[ PHONE UI ]
│
(5. User selects a drive ──► Sends UUID)
│
▼
[ PYTHON WEB BACKEND ]
│
├──► [Has Mountpoint already?] ──► (6A. Use existing path) ──► [ SERVE FILES ]
│
└──► [Mountpoint is null?] ──────► (6B. Create /mnt/[UUID])
│
(7. Run passwordless sudo mount)
│
▼
[ SERVE FILES ]

```

---

## ⚙️ Phase 1: Host OS Configuration

Before booting the web backend, you must authorize the host script to interface with hardware controls safely.

### 1. Configure Passwordless Mount Permissions (`visudo`)
To allow the backend to hook block devices to mount folders natively without popping up a blocking interactive system terminal password request, execute:
```bash
sudo visudo

```

Append the following directive to the very bottom of the file, replacing `yourusername` with your active Linux system username:

```text
yourusername ALL=(ALL) NOPASSWD: /usr/bin/mount, /usr/bin/umount

```

### 2. Define Environment Variables

Create a `.env` file in the project directory to house your localized access criteria:

```text
WEB_PASSWORD="your_chosen_secure_wifi_password"
JWT_SECRET="a_random_long_secret_string_for_signing_tokens"

```

---

## 📦 Phase 2: API Contract Blueprint

The system backend architecture maps directly into the following lightweight FastAPI execution matrix:

### Core Endpoints Matrix

| Endpoint | Method | Operational Description | Active Safety Net |
| --- | --- | --- | --- |
| `/api/auth` | `POST` | Validates local web access password; issues temporary JWT session tokens. | Rate-limiting layers to prevent local Wi-Fi brute forcing. |
| `/api/drives` | `GET` | Parses system blocks via flattened `lsblk`, stripping recovery and internal software disks. | Token validation dependencies execute prior to terminal subprocessing. |
| `/api/drives/connect` | `POST` | Intercepts target UUID. Runs the hybrid mount check sequence. | Strict character sanitization to completely eliminate terminal code injection. |
| `/api/upload` | `POST` | Multi-part form stream moving items via `shutil.copyfileobj()`. | Filename baseline stripping via `os.path.basename()` to counter fake root mappings. |
| `/api/download` | `GET` | Packages and streams target item components via high-performance chunking. | Resolution loop prevents directory traversal outside target bounds. |
| `/api/folder/create` | `POST` | Generates active subdirectories utilizing `os.makedirs(..., exist_ok=True)`. | Special character validation patterns applied to target name arrays. |
| `/api/delete` | `POST` | Triggers target asset elimination (`os.remove` or `shutil.rmtree`). | Hardcoded block prohibiting deletion commands directed at the root mount point. |

---

## 🛡️ Critical Safety Loop (Path Validation)

To guarantee that requests cannot crawl out of the attached drive into your host laptop's private operating system files, every file pipeline route passes requested paths through this core validation check:

```python
def validate_and_resolve_path(user_requested_path: str, active_drive_root: str) -> str:
    # Resolve absolute paths to eliminate internal dynamic links like "../"
    base = os.path.abspath(active_drive_root)
    target = os.path.abspath(os.path.join(base, user_requested_path))
    
    # Block the request if the resolved target path escapes outside the hard drive directory
    if not target.startswith(base):
        raise HTTPException(status_code=403, detail="Traversal Blocked")
    return target

```

---

## 💻 Phase 3: Frontend Interface (UI)

The UI functions as a Single-Page Application (SPA) designed to render as a responsive web layout for mobile viewports.

1. **The Gatekeeper View:** A clean input terminal asking for the configured `WEB_PASSWORD`. On resolution, the payload token is cached securely within local storage.
2. **Hardware Picker View:** Renders responsive cards showing filtered storage items fetched from `/api/drives`, complete with capacity parameters (e.g., `931.5G`). Clicking a card sends the target UUID back to the server.
3. **The Pipeline Terminal View:** Displays current tree contents. Every file array component maps to explicit action triggers:
* 📁 **New Folder:** Fires structural generation payloads to `/api/folder/create`.
* 📤 **Upload File:** Opens the native device filesystem selector, passing standard multi-part data arrays directly to `/api/upload`.
* 📥 **Download Icon:** Spawns targeted download tags hitting `/api/download?relative_file_path=...`.
* 🗑️ **Delete Icon:** Runs a client-side verification popup before passing destructive execution commands to `/api/delete`.



---

## 🌐 Network Deployment

By default, FastAPI binds to localhost (`127.0.0.1`), which blocks external network requests. To allow other devices on your local network to discover the server, you must expose it to your local subnet.

1. Find your host device's local network IP assignment via your network settings (e.g., `192.168.1.15`).
2. Spin up your server environment using Uvicorn, binding explicitly to all local network interfaces:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000

```


3. Open your mobile web browser, point the URL address line directly to your host machine configuration target: `http://192.168.1.15:8000`, enter your access key, and your personal data pipeline is live.

```

```