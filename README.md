# Network Automation & Compliance Toolkit
A Modular Python & Netmiko Framework for Multi-Device Operations and Security Auditing

An enterprise-grade, modular network automation framework built with Python and **Netmiko**. The toolkit decouples operational execution logic from infrastructure parameters to programmatically manage, back up, and audit Cisco IOS network devices over secure shell (SSH) sessions. Designed to replace repetitive manual configuration management, this toolkit implements a reliable pipeline for inventory handling, configuration backup harvesting, and rule-based baseline compliance auditing.

---

## 🚀 Key Features & Enhancements

* **Decoupled Inventory Architecture:** Utilizes an external JSON-formatted asset database (`devices.json`) as a single source of truth, completely eliminating hardcoded credential vulnerabilities.
* **Multi-Device Automation Loop:** Iterates dynamically across multiple network nodes to handle secure authentication and task execution in parallel.
* **Programmatic Configuration Harvesting:** Connects to infrastructure targets via automated SSH to pull raw running configurations and export them into timestamped backup files.
* **Security Compliance Auditing:** Implements programmatic line-by-line parsing of live interface tables to flag missing descriptions on active links and isolate inactive interfaces that violate security baselines by not being properly shut down.
* **Network Timing Safeguards:** Integrates custom timing modifiers (`global_delay_factor` and `fast_cli` overrides) to preserve state stability and prevent premature timeouts over cloud-routed VPN connections.

---

## 📂 Project Directory Structure

```text
network_toolkit/
│
├── devices.json          # Network asset inventory database (Single Source of Truth)
├── main.py               # Interactive central dashboard and engine controller
├── Configuration.py     # Standalone engine for pushing structural configuration sets
│
└── backups/              # Auto-generated directory containing dated system backups
│
└── modules/
    ├── __init__.py
    ├── backup.py         # Automation module handling running-config capture
    └── audit.py          # State-analysis engine processing compliance rulesets
