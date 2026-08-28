<div align="center">

# AkariOS

**A Windows debloat & performance Playbook for AME Beta**

![Version](https://img.shields.io/badge/version-1.0.0-blueviolet)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?logo=windows)
![Playbook](https://img.shields.io/badge/AME%20Beta-Playbook-orange)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## 📖 About

**AkariOS** is a Playbook for [AME Beta](https://amelabs.net/) that strips Windows 10 and Windows 11 of bloatware, telemetry, and background clutter to deliver a cleaner, faster, and more responsive system — while giving you full control over what stays and what goes.

> **⚠️ AkariOS makes deep, irreversible system changes. Always back up your data before applying.**

---

## ✅ Supported Windows Builds

| OS | Version | Build |
|---|---|---|
| Windows 10 | 21H2 | 19044 |
| Windows 10 | 22H2 | 19045 |
| Windows 11 | 22H2 | 22621 |
| Windows 11 | 23H2 | 22631 |
| Windows 11 | 24H2 | 26100 |
| Windows 11 | 25H2 | 26200 |

> Check your build: press `Win + R`, type `winver`, and press Enter.

---

## ⚙️ Configurable Options

During setup, AME Beta will walk you through a series of options. You can enable or disable each one to tailor AkariOS to your needs.

### 🔒 Security
| Option | Default |
|---|---|
| Disable Windows Defender | ✅ Enabled |
| Disable User Account Control (UAC) | Off |
| Disable Process Mitigations | Off |
| Disable Spectre/Meltdown Mitigations | Off |

> ⚠️ Disabling security features reduces system protection. Only do so if you understand the risks.

### 🖥️ Windows Settings
- Dark Mode
- Legacy context menu (Windows 11)
- Legacy Photo Viewer
- Disable VPN services
- Disable Printer / Bluetooth
- Disable Windows Update
- Disable extra power savings

### 🧹 Debloat
| Option | Default |
|---|---|
| Remove Microsoft Edge | ✅ Enabled |
| Remove OneDrive | ✅ Enabled |
| Disable Hyper-V and VBS | Off |
| Install Open-Shell (classic Start menu) | Off |

---

## 🚀 Installation

### Step 1 — Prerequisites

Before you begin, make sure your system is ready:

- ✔️ A **fresh and clean Windows installation** — do not apply AkariOS on top of an existing/modified system

---

### Step 2 — Download AME Beta

Download **AME Beta** from the official Ameliorated website:

👉 **[Download AME Beta](https://download.ameliorated.io/AME%20Beta.zip)**

Extract the ZIP and run **AME Beta.exe**.

---

### Step 3 — Download the AkariOS Playbook

Download the latest **AkariOS Playbook** (`.apbx` file) from the [Releases](../../releases) page of this repository.

> The `.apbx` file is a self-contained package — no extraction needed.

---

### Step 4 — Load the Playbook into AME Beta

There are two ways to load the Playbook:

**Option A — Drag & Drop**
Drag the `AkariOS.apbx` file directly into the sidebar drop zone in AME Beta.

**Option B — Browse**
Click the sidebar slot → click **"use existing"** → select your `.apbx` file.

The Playbook will appear in the sidebar once loaded.

---

### Step 5 — Disable Security (Required)

Click the Playbook in the sidebar and follow the **"Disable Security"** step:

1. AME Beta will open a guided window with toggles.
2. Use the toggles to disable **Windows Defender** via Windows Security.
3. Confirm completion — this unlocks the **"Next"** button.

> AME Beta will warn you if any requirements (pending updates, antivirus, etc.) are not met.

---

### Step 6 — Apply the Playbook

1. Click **"Next"** and accept the license terms.
2. On the options page, configure your desired features (or keep the defaults).
3. Set your user credentials — **remember these**, you'll need them after installation.
4. AME Beta will open a progress window and begin applying AkariOS.
5. Your system will **reboot automatically** during the process — this is normal.

⏱️ Installation typically takes **10–30 minutes** depending on your internet speed and hardware.

---

### 🛠️ Troubleshooting

If something goes wrong during installation:

1. Look for a **yellow error symbol** in the AME Beta window.
2. Click it to open the **Logs folder**.
3. Zip the logs and seek help via:
   - 💬 [Ameliorated Discord](https://discord.gg/kAnuJUPvGX)
   - 📬 [Ameliorated Telegram](https://t.me/+TFCUAzfq6Y-Bl9vG)

---

## 📁 Repository Structure

```
AkariOS-Playbook/
├── Configuration/
│   ├── custom.yml              # Generated monolithic playbook (edit via sections + build script)
│   ├── header.yml              # YAML header (comment block + 'actions:' key)
│   ├── sections/               # Modular section files (01-initialize.yml through 40-end.yml)
│   └── files/                  # Runtime assets deployed to target system
├── Executables/                # PowerShell scripts, C# source, binaries
├── Images/                     # Browser picker images for AME Wizard
├── scripts/
│   ├── split-playbook.py       # One-time: split custom.yml into sections
│   └── build-playbook.py       # Build: concatenate sections → custom.yml
├── playbook.conf               # AME Wizard UI config (feature pages, toggles)
├── playbook.png                # Playbook thumbnail
├── CLAUDE.md                   # AI assistant project memory
└── README.md                   # This file
```

### 🛠️ Development Workflow

The playbook is organized into modular section files under `Configuration/sections/`. AME Wizard requires a single monolithic `custom.yml` file, so a build step is needed after editing sections.

**To edit the playbook:**

1. Edit the relevant file in `Configuration/sections/` (e.g., `10-browsers-*.yml`)
2. Run the build script to regenerate `Configuration/custom.yml`:
   ```bash
   python scripts/build-playbook.py
   ```
3. Commit both the section file(s) and the regenerated `custom.yml`

**Build script flags:**
- `--dry-run` — Preview the generated content without writing
- `--verify` — Compare output against `custom.yml.bak` for byte-identical verification

**Other commands:**
- `python scripts/build-playbook.py --dry-run` — Preview without writing
- `python scripts/split-playbook.py` — One-time: split an existing monolithic `custom.yml` into sections (runs automatically during initial setup, not needed for normal edits)

> **Note:** `Configuration/custom.yml` is a build artifact from the section files. It is committed to the repo so AME Wizard can load it directly — no build step is needed when loading an existing release.

---

## ⚠️ Disclaimer

AkariOS applies deep system modifications that are **difficult or impossible to reverse** without reinstalling Windows. Optional settings — such as disabling UAC, Windows Update, and CPU vulnerability mitigations — will reduce your system's security posture.

> 🛡️ **Windows Defender** can be fully **disabled or re-enabled** at any time through the **AkariOS Companion** tool, so you're never permanently locked out of your security settings.

**Use at your own risk.** This project is not affiliated with Microsoft or Ameliorated LLC.

---

## 🤝 Contributing

Bug reports, suggestions, and pull requests are welcome! If something breaks on your build, please open an issue with:

- Your Windows version and build number
- A description of the problem
- Any relevant logs from AME Beta

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">

Made with 💜 by [isleap9](https://github.com/isleap9) · Powered by [AME Beta](https://amelabs.net/)

</div>
