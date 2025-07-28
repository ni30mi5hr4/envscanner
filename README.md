# 🔍 ENVSCANNER

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Tool-red.svg)](https://github.com)

> 🎯 A high-performance, multi-threaded Laravel `.env` file disclosure scanner that hunts for exposed environment configuration files across multiple hosts and ports.

## ✨ Features

- 🚀 **Multi-threaded scanning** - Lightning-fast concurrent processing
- 🎯 **Multiple endpoint detection** - Scans `/.env`, `/.env.backup`, `/.env.old`, and more
- 🔍 **Smart pattern matching** - Intelligent detection of Laravel environment variables
- 📊 **JSON output** - Structured results for easy analysis
- 🌈 **Colorized terminal output** - Beautiful, readable console interface
- ⚡ **Custom port scanning** - Configurable port lists for targeted scanning
- 📈 **Real-time statistics** - Live scan progress and hit counters

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/envscanner.git
cd envscanner
pip install -r requirements.txt
```

### 📦 Dependencies
```txt
requests
colorama  
urllib3
```

## 🚀 Usage

### Basic Command
```bash
python envscanner.py -i targets.txt -o results.json
```

### ⚙️ Command Line Options

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `-i, --input` | 📁 Input file with target hosts | **Required** | `hosts.txt` |
| `-o, --output` | 💾 Output JSON file for results | **Required** | `results.json` |
| `--threads` | 🧵 Number of concurrent threads | `200` | `--threads 100` |
| `--ports` | 🔌 Comma-separated port list | `80,443,8080` | `--ports 80,443,8000` |

### 💡 Usage Examples

**🔥 Quick Scan:**
```bash
python envscanner.py -i hosts.txt -o findings.json
```

**⚡ High-Performance Scan:**
```bash
python envscanner.py -i targets.txt -o results.json --threads 500 --ports 80,443,8000,8080,9000
```

**🎯 Focused Web Server Scan:**
```bash
python envscanner.py -i webservers.txt -o env_leaks.json --threads 50 --ports 80,443
```

## 📝 Input Format

Create a text file with one host per line:
```txt
example.com
192.168.1.100
subdomain.target.com
api.company.com
```

## 📤 Output Format

Results are saved in structured JSON format:
```json
{
  "url": "https://example.com/.env",
  "status_code": 200,
  "keys": ["APP_KEY", "DB_PASSWORD", "MAIL_PASSWORD", "AWS_ACCESS_KEY_ID"],
  "env_dump": "APP_NAME=Laravel\nAPP_KEY=base64:xyz123...\nDB_PASSWORD=secret123"
}
```

## 🔎 Detected Variables

The scanner identifies critical Laravel environment variables:

- 🗄️ **Database:** `DB_HOST`, `DB_PASSWORD`, `DB_USERNAME`, `DB_DATABASE`
- 🔑 **Application:** `APP_KEY`, `APP_ENV`, `APP_DEBUG`, `APP_URL`
- 📧 **Mail:** `MAIL_HOST`, `MAIL_USERNAME`, `MAIL_PASSWORD`
- ☁️ **AWS:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_BUCKET`
- 📡 **Cache/Queue:** `REDIS_PASSWORD`, `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`
- 🔐 **Sessions:** `SESSION_DRIVER`, `SESSION_LIFETIME`

## 📊 Sample Output

```
 ███████╗███╗   ██╗██╗   ██╗
 ██╔════╝████╗  ██║██║   ██║
 █████╗  ██╔██╗ ██║██║   ██║
 ██╔══╝  ██║╚██╗██║██║   ██║
 ███████╗██║ ╚████║╚██████╔╝
 ╚══════╝╚═╝  ╚═══╝ ╚═════╝ 

   Laravel .env Disclosure Scanner
         by ni30mi5hr4

[FOUND] https://target.com/.env | Keys: APP_KEY, DB_PASSWORD, MAIL_PASSWORD

📊 Scan Summary:
 - Total Scanned  : 1500
 - Total Hits     : 23
 - Total Failures : 1477

✅ Results saved to: results.json
```

## ⚠️ Disclaimer

🛡️ **Important:** This tool is designed for **authorized security testing only**. Always ensure you have explicit written permission before scanning any targets. Unauthorized scanning may violate laws and regulations.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**ni30mi5hr4** - *Security Researcher*

---

<div align="center">

**⭐ Star this repo if you found it useful! ⭐**

*Made with ❤️ for the security community*

</div>
