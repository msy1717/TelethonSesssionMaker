# 📱 Telethon Multi-Session Maker

A powerful and user-friendly CLI tool to create multiple Telegram sessions from phone numbers with a beautiful terminal interface.

## ✨ Features

- 🎨 **Beautiful Terminal Interface** - Rich, colorful CLI with progress bars and panels
- 📋 **Bulk Session Creation** - Create multiple sessions from a CSV file
- 🔐 **Flexible API Configuration** - Support for single or multiple API credentials
- 💾 **No Config Files Required** - Run directly from terminal with interactive prompts
- ⚡ **Error Handling** - Comprehensive error handling with clear messages
- 🛡️ **2FA Support** - Full support for two-factor authentication
- 📊 **Session Summary** - Detailed report of successful and failed sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Telegram API credentials (get from https://my.telegram.org/apps)

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install telethon rich
```

### Usage

Simply run the script:
```bash
python main.py
```

The tool will guide you through the process interactively!

## 📝 Usage Methods

### Method 1: Interactive Mode (Recommended)

Just run the script and follow the prompts:

```bash
python main.py
```

You'll be asked to:
1. Provide phone numbers (from CSV or create example)
2. Choose API credential source (CSV file or manual entry)
3. Enter API credentials if needed
4. Confirm and start session creation

### Method 2: Using CSV Files

#### Step 1: Create `phone.csv`

Create a file named `phone.csv` with one phone number per line:

```
+1234567890
+9876543210
+1122334455
```

**Important:** Include country code with `+` prefix

#### Step 2: Create `api.csv` (Optional)

If you want to use different API credentials for each phone:

```csv
123456,abcdef1234567890abcdef1234567890
789012,fedcba0987654321fedcba0987654321
345678,1234567890abcdef1234567890abcdef
```

Format: `api_id,api_hash`

**Note:** You can also enter API credentials interactively when running the script.

#### Step 3: Run the Script

```bash
python main.py
```

## 🔑 Getting API Credentials

1. Visit https://my.telegram.org/apps
2. Log in with your phone number
3. Create a new application
4. Copy your `api_id` and `api_hash`

## 📂 File Structure

```
.
├── main.py              # Main script
├── phone.csv            # Your phone numbers (you create this)
├── api.csv              # Your API credentials (optional)
├── phone.csv.example    # Example phone numbers file
├── api.csv.example      # Example API credentials file
├── sessions/            # Generated session files (auto-created)
│   └── *.session       # Telegram session files
└── README.md           # This file
```

## 💡 Features Explained

### Single vs Multiple API Credentials

**Single API (Default):**
- Use one API ID/Hash for all phone numbers
- Simpler setup
- Good for personal use

**Multiple APIs:**
- Use different API credentials for each phone
- Better for bulk operations
- Reduces rate limiting risk

### Session Files

- Session files are saved in the `sessions/` directory
- File format: `{phone_number}.session`
- These files contain authentication data
- Keep them secure and private!

## 🛠️ Advanced Usage

### Command Line Direct Run

```bash
# Make script executable (Linux/Mac)
chmod +x main.py
./main.py

# Windows
python main.py
```

### Example Workflow

1. **First Run** (creates example files):
```bash
python main.py
# Creates phone.csv.example and api.csv.example
```

2. **Edit your files**:
```bash
# Copy examples and edit
cp phone.csv.example phone.csv
# Add your phone numbers to phone.csv
```

3. **Run again**:
```bash
python main.py
# Follow interactive prompts
```

## ⚠️ Important Notes

- **Rate Limiting**: Telegram has rate limits. Don't create too many sessions too quickly
- **2FA**: If you have two-factor authentication enabled, you'll be prompted for your password
- **Security**: Never share your session files or API credentials
- **Phone Format**: Always use international format with `+` (e.g., `+1234567890`)
- **Sessions Storage**: Keep your `sessions/` folder backed up and secure

## 🐛 Troubleshooting

### "Phone number invalid"
- Make sure to include country code with `+` prefix
- Example: `+1234567890` not `1234567890`

### "API ID invalid"
- Check your API credentials from https://my.telegram.org/apps
- Make sure API ID is a number
- API Hash should be a 32-character string

### "Flood wait error"
- You've hit Telegram's rate limit
- Wait the specified time before trying again
- Consider using multiple API credentials

### Import errors
- Make sure you installed dependencies: `pip install telethon rich`
- Try: `pip install --upgrade telethon rich`

## 📋 Requirements

```
telethon>=1.24.0
rich>=13.0.0
```

## 🔒 Security Best Practices

1. **Never commit sensitive files to git**
   - `phone.csv` - Contains your phone numbers
   - `api.csv` - Contains your API credentials
   - `sessions/*.session` - Contains authentication data

2. **Keep API credentials secure**
   - Don't share your API ID and Hash
   - Each person should use their own credentials

3. **Protect session files**
   - These files give full access to your Telegram account
   - Store them securely
   - Don't share them with anyone

## 📞 Support & Contact

**Developer:** [@GodmrunaL](https://t.me/GodmrunaL)  
**Telegram Channel:** [@Beastx_Bots](https://t.me/Beastx_Bots)

Need more tools or have questions? Join our channel!

## 📄 License

This tool is provided as-is for educational and personal use.

## 🙏 Credits

- **Developer:** @GodmrunaL
- **Channel:** @Beastx_Bots
- **Built with:** [Telethon](https://github.com/LonamiWebs/Telethon) & [Rich](https://github.com/Textualize/rich)

---

**⭐ If you find this tool useful, please star the repository and share it with others!**

**Need more Telegram tools? Join @Beastx_Bots on Telegram!**
