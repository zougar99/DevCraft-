# 🔨 DevCraft- — Multi-tool project: Flask task manager web app + ADB-based Android region spoofer for rooted devices

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/zougar99/DevCraft-/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zougar99/DevCraft-?style=social)](https://github.com/zougar99/DevCraft-)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)](https://github.com/zougar99/DevCraft-)

> Multi-tool project: Flask task manager web app + ADB-based Android region spoofer for rooted devices.

---

## 📖 Table of Contents
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features
- ✔ **Flask Task Manager** — Full CRUD web app with user auth and SQLite backend
- ✔ **ADB Spoofer** — Android region/location spoofer via ADB for rooted devices
- ✔ **REST API** — Task manager exposes RESTful endpoints for external integration
- ✔ **GPS Spoofing** — Mock GPS location with ADB commands
- ✔ **Device Profiles** — Save and switch between location profiles
- ✔ **Logging** — Comprehensive logging for all ADB operations

---

## 🔮 How It Works

```
  Input ──► Processing Pipeline ──► Output
  ┌────────┐   ┌────────┐   ┌────────┐
  │ Data   │──►│ Engine │──►│ Result │
  │ Source │   │ Logic  │   │        │
  └────────┘   └────────┘   └────────┘
```

1. **Input** — Load data from file, API, or user input
2. **Process** — Core engine applies logic/analysis/transformation
3. **Output** — Results displayed in UI, saved to file, or sent via API

---

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Database | SQLite / SQLAlchemy |
| Mobile | ADB (Android Debug Bridge) |
| UI | HTML + Bootstrap (web) |
| Platform | Windows / Linux (host) + Android (device) |

---

## 🚀 Installation

```bash
git clone https://github.com/zougar99/DevCraft-.git
cd DevCraft-
pip install -r requirements.txt
```

---

## 📄 Configuration

Create a `config.yaml` or `.env` file in the project root:

```yaml
# Application settings
debug: false
port: 8080
theme: dark
language: en
```

---

## 🧰 Usage Guide

**Task Manager:**
1. `python app.py` — starts Flask server on :5000
2. Open browser at http://localhost:5000

**ADB Spoofer:**
1. Connect rooted Android device via USB
2. `python spoof.py --lat 48.85 --lng 2.35`
3. Phone GPS now reports Paris coordinates

---

## 🖼 Screenshots

> *(Screenshots coming soon. PRs welcome!)*

---

## 🔄 Roadmap

- 🟢 Web dashboard
- 🟡 Mobile companion app
- ⚫ API access
- ⚫ Plugin system
- ⚫ Multi-language support

---

## ❓ FAQ

### Does spoofing require root?
Yes — `adb root` access is required for GPS spoofing.

### Can I use this for production task management?
The Flask app is suitable for small teams / personal use.

---

## 🚧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **App won't start** | Check Python version (3.10+); run `pip install -r requirements.txt` |
| **No output** | Check logs in `logs/` folder; enable debug mode in config |
| **Performance issues** | Close other applications; reduce batch size in config |
| **Dependency errors** | Create fresh venv: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📐 License
Distributed under the **MIT License**. See [`LICENSE`](https://github.com/zougar99/DevCraft-/blob/main/LICENSE) for more information.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/zougar99">zougar99</a>
</p>
