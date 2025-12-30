# DetectMe

**Professional OSINT (Open Source Intelligence) Tool for Apple Devices**

DetectMe is a comprehensive information gathering tool designed exclusively for macOS and iOS devices. It enables security professionals, researchers, and organizations to gather publicly available information about domains, usernames, phone numbers, and email addresses for legitimate security research, brand monitoring, and educational purposes.

---

## ⚠️ Legal Disclaimer & Terms of Use

### Intended Use

**DetectMe is designed for legitimate purposes only:**

- ✅ **Security Research**: Vulnerability assessment and penetration testing (with proper authorization)
- ✅ **Brand Monitoring**: Tracking brand mentions and potential impersonation
- ✅ **Educational Purposes**: Learning OSINT methodologies and information security
- ✅ **Self-Learning**: Understanding public data gathering techniques
- ✅ **Legitimate Investigations**: Authorized security audits and compliance checks
- ✅ **Threat Intelligence**: Gathering publicly available threat information

### Prohibited Use

**This tool must NOT be used for:**

- ❌ Unauthorized access to systems or data
- ❌ Harassment, stalking, or doxxing
- ❌ Privacy violations or unauthorized surveillance
- ❌ Any activity violating local or international laws
- ❌ Gathering information without proper authorization
- ❌ Any malicious or illegal activities

### User Responsibility

By using DetectMe, you acknowledge and agree that:

1. You will only use this tool for legal, authorized purposes
2. You have obtained proper authorization before investigating any target
3. You understand and accept full responsibility for your actions
4. You will comply with all applicable laws and regulations
5. The developers and contributors are not responsible for misuse

**This tool is provided "as-is" for educational and legitimate security research purposes. Use at your own risk and ensure compliance with all applicable laws.**

---

## 🍎 Platform Support

- **macOS**: Fully supported with native GUI
- **iOS**: Command-line interface supported
- **Windows**: Not supported (Apple devices only)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- macOS or iOS device
- Internet connection
- (Optional) API keys for enhanced features

### Installation

#### Standard Installation

```bash
git clone <repository-url>
cd DetectMe
chmod +x install.sh
./install.sh
```

#### Virtual Environment Installation (Recommended)

```bash
git clone <repository-url>
cd DetectMe
python3 -m venv .venv
source .venv/bin/activate
chmod +x install.sh
./install.sh
pip3 install -r requirements.txt
```

### Running the Application

#### Command Line Interface

```bash
cd DetectMe
source .venv/bin/activate  # If using virtual environment
python3 AppleOSINT.py
```

#### Graphical User Interface

```bash
python3 AppleOSINT.py
# Select option 8 (GUI Mode)
```

#### Using the Launcher

```bash
./Launchers/macOS_Launcher.sh
```

---

## 📋 Core Features

### 1. Username Lookup
Search for usernames across 25+ social media platforms and services:
- Social Networks: Twitter, Facebook, Instagram, LinkedIn, Reddit
- Developer Platforms: GitHub, Stack Overflow, CodePen, Dev.to
- Media Platforms: YouTube, TikTok, Vimeo, SoundCloud, Spotify
- Professional Networks: Behance, Dribbble, Medium
- And many more...

**Use Cases**: Brand monitoring, impersonation detection, social media analysis

### 2. Domain Information Analysis
Comprehensive domain intelligence gathering:
- **WhoIS Data**: Registrar information, registration dates, expiration
- **DNS Records**: A, AAAA, MX, NS, TXT, CNAME records
- **SSL Certificates**: Certificate details, validity, issuer information
- **Subdomain Discovery**: Identify associated subdomains
- **IP Resolution**: Domain to IP address mapping

**Use Cases**: Security audits, domain monitoring, infrastructure analysis

### 3. Phone Number Lookup & Geolocation
Advanced phone number analysis with location mapping:
- Country and carrier identification
- Timezone information
- **Precise Location Mapping**: City-level geolocation using area codes
- Automatic interactive map generation
- Number formatting (International, National, E.164)

**Use Cases**: Fraud detection, location verification, carrier analysis

### 4. Email Lookup
Email address analysis and service association:
- Service registration checking
- Breach data verification (via Have I Been Pwned)
- Profile association detection

**Use Cases**: Security audits, account verification, breach monitoring

### 5. Google Dorks
Advanced Google search capabilities:
- File type searches (PDF, DOC, etc.)
- Site-specific searches
- Date range filtering
- Image and video searches

**Use Cases**: Security research, information discovery, content analysis

### 6. Interactive Geolocation Maps
Automatic generation of interactive maps:
- Precise location markers with coordinates
- Custom labels and information popups
- Zoom controls and fullscreen mode
- Measurement tools
- Multiple map styles (Light, Dark, Minimal)

**Use Cases**: Location visualization, geographic analysis, route planning

### 7. Information Graphs
Network visualization and relationship mapping:
- Visualize connections between entities
- Node and edge representations
- Export as high-resolution PNG
- Customizable layouts

**Use Cases**: Relationship analysis, network mapping, data visualization

### 8. Report Management
Comprehensive report handling:
- JSON format reports with timestamps
- Report encoding/decoding for security
- QR code generation for file transfer
- Organized storage in Reports directory

---

## ⚙️ Configuration

### API Keys

For enhanced functionality, configure API keys in `Configuration/Configuration.ini`:

```ini
[API]
WhoIS_API_Key = your_api_key_here
Shodan_API_Key = your_shodan_key_here
```

**WhoIS API**: Get your API key from [whois.whoisxmlapi.com](https://whois.whoisxmlapi.com)

### Proxy Configuration

Enable proxy support for anonymous requests:

```ini
[Proxy]
Enabled = True
Type = http
Host = proxy.example.com
Port = 8080
Username = your_username
Password = your_password
```

### Theme Configuration

Customize the interface theme in `GUI/Theme/Mode.json`:

```json
{
    "Color": {
        "Background": "Dark"
    }
}
```

**Available Themes**: `Light`, `Dark`, `High-Contrast`

---

## 🏗️ Architecture

### Project Structure

```
DetectMe/
├── AppleOSINT.py          # Main application entry point
├── Core/                  # Core OSINT modules
│   ├── Main.py           # Application controller
│   ├── UsernameLookup.py # Username search across platforms
│   ├── DomainLookup.py   # Domain intelligence gathering
│   ├── PhoneLookup.py    # Phone number analysis
│   ├── EmailLookup.py    # Email service checking
│   ├── GoogleDorks.py    # Advanced Google searches
│   ├── Geolocation.py    # IP and location services
│   ├── MapGenerator.py   # Interactive map creation
│   ├── GraphGenerator.py # Network visualization
│   ├── ProxyManager.py   # Proxy configuration
│   ├── ReportEncoder.py  # Report encryption/decryption
│   └── QRCodeGenerator.py # QR code generation
├── GUI/                   # Graphical user interface
│   ├── App.py           # Modern GUI application
│   ├── Theme/           # Theme configuration
│   ├── Credentials/     # Authentication settings
│   └── Language/        # Localization files
├── Configuration/         # Configuration files
│   └── Configuration.ini
├── Launchers/            # Platform-specific launchers
│   └── macOS_Launcher.sh
└── Reports/              # Generated reports (gitignored)
```

---

## 📊 Report Formats

All search results are automatically saved in the `Reports/` directory:

- **Username Reports**: `username_<username>_<timestamp>.json`
- **Domain Reports**: `domain_<domain>_<timestamp>.json`
- **Phone Reports**: `phone_<number>_<timestamp>.json`
- **Email Reports**: `email_<email>_<timestamp>.json`
- **Dork Reports**: `dorks_<query>_<timestamp>.json`
- **Maps**: `map_<timestamp>.html`
- **Graphs**: `graph_<timestamp>.png`

Reports include timestamps, detailed results, and location data when available.

---

## 🔒 Security Features

- **Report Encryption**: Encode sensitive reports for secure storage
- **Proxy Support**: Route requests through proxies for anonymity
- **Configuration Protection**: Sensitive config files are gitignored
- **Secure Storage**: Reports directory excluded from version control

---

## 💼 Professional Use Cases

### Security Teams
- Vulnerability assessment and penetration testing
- Threat intelligence gathering
- Security audit support
- Incident response investigations

### Brand Protection
- Brand monitoring and impersonation detection
- Social media presence analysis
- Domain squatting identification
- Reputation management

### Research & Education
- OSINT methodology training
- Information security education
- Public data analysis research
- Academic security research

### Compliance & Auditing
- Authorized security audits
- Compliance verification
- Due diligence investigations
- Risk assessment support

---

## 🛠️ Technical Requirements

- **Python**: 3.10 or higher
- **Operating System**: macOS 10.15+ or iOS
- **Dependencies**: See `requirements.txt`
- **Internet**: Required for API calls and lookups
- **Storage**: ~100MB for installation, additional space for reports

---

## 📚 Documentation

### Getting Started
1. Review this README for installation and basic usage
2. Configure API keys in `Configuration/Configuration.ini` for enhanced features
3. Run the application and explore the menu options
4. Check the `Reports/` directory for generated results

### Advanced Usage
- Customize themes in `GUI/Theme/Mode.json`
- Configure proxy settings for anonymous requests
- Use report encoding for sensitive data protection
- Generate QR codes for easy report sharing

---

## 🤝 Contributing

We welcome contributions from the security and open-source community. Please ensure:

- Code follows Python best practices
- All changes are tested on macOS
- Documentation is updated accordingly
- Legal and ethical guidelines are strictly followed
- Pull requests include clear descriptions

---

## 📄 License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

---

## ⚠️ Final Reminder

**DetectMe is a professional tool designed for legitimate security research, brand monitoring, and educational purposes.**

- ✅ Use responsibly and ethically
- ✅ Obtain proper authorization before investigations
- ✅ Respect privacy and comply with all laws
- ✅ Follow your organization's security policies
- ❌ Do not use for illegal or unauthorized activities

**The developers and contributors are not responsible for misuse of this tool. Users are solely responsible for ensuring their use complies with all applicable laws and regulations.**

---

## 📞 Support

For issues, questions, or contributions:
- Review the documentation in this README
- Check configuration files for setup issues
- Ensure all dependencies are properly installed
- Verify you have proper authorization for your use case

---

**DetectMe - Professional OSINT Tool for Apple Devices**

*Built for security professionals, researchers, and organizations committed to ethical information gathering.*
