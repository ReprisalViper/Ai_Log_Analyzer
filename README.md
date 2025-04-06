# 🧠 AI-Powered Log Analyzer (WIP)

A smart, machine-learning-powered tool to detect anomalies in server logs. Built with Python, Flask, Docker, and PostgreSQL. Designed for cybersecurity use cases like intrusion detection, behavioral monitoring, and log forensics.

> ⚠️ **Note:** This project is still under development. Features like a frontend dashboard and additional security enhancements are coming soon.

---

## 🤝 Contributor  
- **Yugveer Singh Sidhu** – [@ReprisalViper](https://github.com/ReprisalViper)

## 🚀 Features

- 🔍 Parses Apache-style logs
- 🧠 Uses Isolation Forest for anomaly detection
- 💾 Stores parsed logs in PostgreSQL
- 📤 Upload logs via API using `curl` or Postman
- 🐳 Dockerized for easy deployment

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Flask** (API layer)
- **scikit-learn** (machine learning)
- **PostgreSQL** (data storage)
- **Docker** + **Docker Compose** (containerization)

---

## 📦 Getting Started (Docker)

### 1. Clone the repo

```bash
git clone https://github.com/reprisalviper/ai-log-analyzer.git
cd ai-log-analyzer
