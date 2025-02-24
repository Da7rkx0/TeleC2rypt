# TeleC2rypt - Telegram-Based Remote Administration Tool

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

TeleC2rypt is a powerful Windows remote administration tool that operates through Telegram, providing secure and stealthy system control capabilities.

## 🚀 Features

### 💻 System Control
- Full system information retrieval
- Process management and monitoring
- Service control and configuration
- Registry manipulation capabilities
- Scheduled task management

### 🌐 Network Management
- Network configuration control
- Connection monitoring
- Firewall management
- Advanced networking tools

### 📂 File Operations
- File system navigation
- File upload/download capabilities
- Directory manipulation
- File attribute management

### 🔒 Security Features
- User authentication
- Session management
- Permission control
- Command validation

### 📸 Monitoring
- Screenshot capability
- System status monitoring
- Event log access
- Performance tracking

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TeleC2rypt.git
cd TeleC2rypt
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
# Create .env file with your settings
TELEGRAM_TOKEN=your_bot_token
ALLOWED_USER_ID=your_telegram_id
```

4. Build the executable:
```bash
python build.py
```

## 📝 Usage

### Basic Commands
```
/start - Initialize connection
/help - Show available commands
/screenshot - Take screenshot
/download <path> - Download file
/upload - Upload file to system
```

### System Commands
```
systeminfo - Get system information
tasklist - List running processes
netstat - Show network connections
reg query - Query registry
```

### File Management
```
dir - List directory contents
type - View file contents
copy - Copy files
del - Delete files
```

## 🔧 Configuration

The tool can be configured through the following files:
- `.env`: Environment variables and tokens
- `requirements.txt`: Python dependencies
- `build.py`: Build configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Users are responsible for compliance with all applicable laws. The authors assume no liability for misuse or damage.

## 🙏 Acknowledgments

- Python Telegram Bot library
- PyInstaller
- PyAutoGUI

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Telegram: [@yourusername](https://t.me/yourusername)

---
Made with ❤️ by [Your Name]
