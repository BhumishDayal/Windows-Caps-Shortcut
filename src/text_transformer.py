"""Cross-platform reference port of TextTransformer.ahk. Needs `keyboard` and
`pyperclip`; on Windows the AHK build is the recommended runtime."""

from __future__ import annotations

import logging
import re
import sys
import time
from pathlib import Path
from typing import Callable

LOG = logging.getLogger("text_transformer")

CLIPBOARD_TIMEOUT = 0.8
RESTORE_DELAY = 0.2
MAX_LENGTH = 0

DEFAULT_BRANDS = [
    "iPhone", "iPad", "iPod", "iMac", "iCloud", "iOS", "iPadOS", "macOS",
    "watchOS", "tvOS", "iWork", "iMovie", "iTunes", "iBooks", "FaceTime",
    "FaceID", "TouchID", "MacBook", "AirPods", "AirTag", "AirPlay", "AirDrop",
    "HomePod", "AppleCare", "AppleScript",
    "PowerPoint", "OneDrive", "OneNote", "SharePoint", "PowerShell", "PowerBI",
    "PowerToys", "IntelliSense", "ReSharper", "VBScript", "JScript", "DirectX",
    "JavaScript", "TypeScript", "CoffeeScript", "ActionScript", "PostScript",
    "LiveScript",
    "Node.js", "Next.js", "Nuxt.js", "Vue.js", "Three.js", "Express.js",
    "Nest.js", "jQuery", "FastAPI", "NestJS", "RxJS",
    "GraphQL", "PostgreSQL", "MySQL", "NoSQL", "MongoDB", "MariaDB", "DynamoDB",
    "CockroachDB", "ElasticSearch", "OpenSearch", "ClickHouse", "DuckDB",
    "PlanetScale", "Supabase", "Firebase", "BigQuery", "BigTable", "RocksDB",
    "SurrealDB", "EdgeDB", "FaunaDB",
    "GitHub", "GitLab", "BitBucket", "GitOps", "GitFlow", "GitKraken",
    "JetBrains", "IntelliJ", "PyCharm", "WebStorm", "RubyMine", "GoLand",
    "DataGrip", "AppCode", "TeamCity", "SourceTree", "NetBeans",
    "TensorFlow", "PyTorch", "OpenCV", "OpenAI", "ChatGPT", "DeepMind",
    "DeepSeek", "HuggingFace", "MidJourney",
    "OpenStack", "OpenShift", "OpenSSH", "OpenSSL", "OpenJDK", "OpenWRT",
    "OpenLDAP", "OpenSUSE", "OpenID",
    "FreeBSD", "OpenBSD", "NetBSD", "DragonFlyBSD", "ChromeOS", "ChromeBook",
    "LineageOS", "GrapheneOS",
    "WordPress", "WooCommerce", "BigCommerce", "SoundCloud", "MailChimp",
    "MailGun", "FedEx", "eBay", "GoFundMe", "GoDaddy", "GoPro", "DuckDuckGo",
    "MetaMask", "ProtonMail", "ProtonVPN", "DataDog", "PagerDuty", "HashiCorp",
    "JPMorgan", "DreamWorks", "ResearchGate",
    "DevOps", "FinOps", "MLOps", "DataOps", "AIOps",
    "PayPal", "ApplePay", "GooglePay", "AmazonPay", "SamsungPay", "AliPay",
    "WhatsApp", "LinkedIn", "YouTube", "TikTok", "SnapChat", "WeChat", "KakaoTalk",
    "TeX", "LaTeX", "BibTeX", "XeTeX", "LuaTeX", "JSDoc", "TypeDoc", "JavaDoc",
    "WebGL", "WebRTC", "WebAssembly", "WebSocket",
    "SaaS", "PaaS", "IaaS", "FaaS",
    "OAuth", "PhD", "MSc", "BSc", "DALL-E", "PlayStation", "Bluetooth",
]
BRANDS = {b.lower(): b for b in DEFAULT_BRANDS}

# Don't add words that are also common English (IS, IT, AS, REST, RADIUS, HID,
# LED, ASP, ANN, ...) - they'd corrupt Title Case. test_acronym_list_excludes_
# common_english_words guards a representative subset.
DEFAULT_ACRONYMS = {
    "2FA", "AAA", "AAC", "ABAC", "ABI", "ACID", "ACK", "ACL",
    "ACM", "ACPI", "ADC", "ADO", "ADSL", "ADT", "AES", "AGI",
    "AGP", "AHCI", "AI", "AMOLED", "AMQP", "ANSI", "AOP", "AOT",
    "APFS", "API", "APK", "APU", "AR", "ARGB", "ARP", "ARPA",
    "ARPANET", "ARR", "ASAP", "ASCII", "ASIC", "ASLR", "ASN", "AST",
    "ATA", "AUP", "AV", "AVC", "AVI", "AWT", "B2B", "B2C",
    "B2E", "BBS", "BCC", "BCD", "BCP", "BDD", "BERT", "BFS",
    "BGP", "BIOS", "BMP", "BOM", "BPM", "BSD", "BSS", "BYOD",
    "CAC", "CAD", "CAE", "CAM", "CAPTCHA", "CASB", "CCM", "CCTV",
    "CD", "CDE", "CDMA", "CDN", "CDP", "CEO", "CFG", "CFO",
    "CGI", "CI", "CIA", "CIDR", "CIFS", "CIM", "CIO", "CISA",
    "CISC", "CISO", "CJK", "CLI", "CMDB", "CMM", "CMMI", "CMO",
    "CMOS", "CMS", "CMYK", "CNC", "CNN", "COB", "COBOL", "COO",
    "CORBA", "CORS", "COTS", "CPAN", "CPU", "CRC", "CRLF", "CRM",
    "CRT", "CRUD", "CS", "CSO", "CSP", "CSR", "CSRF", "CSS",
    "CSV", "CTO", "CTR", "CV", "CVE", "CVS", "CVSS", "CX",
    "DAC", "DAO", "DAS", "DAU", "DBA", "DBMS", "DCOM", "DDL",
    "DDR", "DDoS", "DEB", "DEP", "DES", "DFS", "DHCP", "DHTML",
    "DIMM", "DIY", "DKIM", "DLC", "DLL", "DLP", "DMA", "DMARC",
    "DMCA", "DMG", "DMI", "DML", "DMV", "DMZ", "DNAT", "DNS",
    "DOCSIS", "DOD", "DOJ", "DOM", "DOS", "DPI", "DPO", "DRAM",
    "DRM", "DSL", "DSN", "DSP", "DSS", "DTD", "DTLS", "DTO",
    "DVI", "DVR", "EAP", "EBCDIC", "EBITDA", "EBS", "EC2", "ECC",
    "ECDSA", "ECMA", "EDA", "EDI", "EDR", "EEPROM", "EFI", "EFS",
    "EIGRP", "EMI", "ENIAC", "EOD", "EOF", "EOL", "EOM", "EOW",
    "EPROM", "ERD", "ERP", "ESB", "ETA", "ETL", "ETW", "EU",
    "EULA", "EV", "EVP", "EXE", "FAA", "FAQ", "FBI", "FCC",
    "FDA", "FDD", "FDDI", "FDE", "FET", "FHS", "FIFO", "FIPS",
    "FLAC", "FLOPS", "FLV", "FOSS", "FPGA", "FPS", "FPU", "FQDN",
    "FSB", "FSF", "FSM", "FTC", "FTP", "FTPS", "FUD", "FYI",
    "GAN", "GB", "GCC", "GCM", "GCP", "GDB", "GDPR", "GID",
    "GIF", "GIS", "GNU", "GPG", "GPGPU", "GPL", "GPO", "GPRS",
    "GPT", "GPU", "GRE", "GSM", "GTK", "GTM", "GUI", "GUID",
    "HAL", "HBA", "HCI", "HCL", "HDD", "HDL", "HDMI", "HEX",
    "HIPAA", "HMAC", "HMI", "HPC", "HR", "HSL", "HSM", "HSV",
    "HTML", "HTTP", "HTTPS", "IAM", "IANA", "IBM", "ICANN", "ICMP",
    "ICS", "ICT", "ID", "IDE", "IDS", "IEC", "IEEE", "IETF",
    "IGMP", "IIS", "IMAP", "IP", "IPA", "IPC", "IPMI", "IPO",
    "IPS", "IPSEC", "IPTV", "IPX", "IRC", "IRQ", "IRS", "ISA",
    "ISDN", "ISO", "ISP", "ISR", "ISV", "ITIL", "ITU", "JBOD",
    "JCL", "JDBC", "JDK", "JIT", "JMS", "JNI", "JPEG", "JPG",
    "JRE", "JS", "JSON", "JSP", "JTAG", "JVM", "JWE", "JWS",
    "JWT", "KB", "KDC", "KDE", "KDF", "KMS", "KPI", "KVM",
    "LACP", "LAMP", "LAN", "LBA", "LCD", "LDAP", "LFI", "LGPL",
    "LIFO", "LLC", "LLM", "LOC", "LRU", "LSB", "LSI", "LSP",
    "LTE", "LTL", "LTR", "LTS", "LTV", "LUN", "LVM", "LZW",
    "MAC", "MAPI", "MAU", "MBR", "MDM", "MDR", "MFA", "MFT",
    "MIB", "MIDI", "MIME", "MIMO", "MIPS", "MKV", "ML", "MMC",
    "MMO", "MMORPG", "MMU", "MOSFET", "MOTD", "MOU", "MOV", "MP3",
    "MP4", "MPEG", "MPLS", "MQTT", "MRR", "MSA", "MSB", "MSI",
    "MSP", "MSSP", "MTBF", "MTTF", "MTTR", "MTU", "MUA", "MVC",
    "MVP", "NAC", "NAK", "NAS", "NASA", "NAT", "NATO", "NDA",
    "NDP", "NFA", "NFC", "NFS", "NGFW", "NIC", "NIST", "NLE",
    "NLG", "NLP", "NLU", "NMI", "NNTP", "NOC", "NOP", "NPC",
    "NPU", "NSA", "NTFS", "NTLM", "NTP", "NUMA", "NVD", "NVMe",
    "NVR", "NVRAM", "OCR", "OCSP", "ODBC", "OEM", "OFDM", "OGG",
    "OID", "OKR", "OLA", "OLAP", "OLE", "OLED", "OLTP", "OOM",
    "OOP", "OOTB", "ORM", "OS", "OSI", "OSINT", "OSPF", "OTP",
    "OUI", "OWASP", "P2P", "PAM", "PBX", "PC", "PCB", "PCI",
    "PCIe", "PCM", "PCRE", "PDA", "PDF", "PEM", "PFS", "PGP",
    "PHI", "PHP", "PID", "PII", "PKCS", "PKI", "PLC", "PNG",
    "POP3", "POSIX", "PPP", "PPTP", "PR", "PRNG", "PSK", "PSTN",
    "PSU", "PTO", "PXE", "QA", "QC", "QEMU", "QR", "RAG",
    "RAID", "RAII", "RAM", "RARP", "RBAC", "RCA", "RDBMS", "RDP",
    "RDS", "RFB", "RFC", "RFI", "RFID", "RFP", "RFQ", "RGB",
    "RGBA", "RISC", "RLHF", "RMI", "RNN", "ROI", "ROM", "RPA",
    "RPC", "RPG", "RPM", "RPO", "RSA", "RSI", "RSS", "RST",
    "RSVP", "RTC", "RTL", "RTOS", "RTP", "RTSP", "RTT", "RWD",
    "SAML", "SAS", "SASE", "SASL", "SATA", "SCADA", "SCCM", "SCM",
    "SCP", "SCSI", "SCSS", "SDK", "SDLC", "SDN", "SDR", "SDRAM",
    "SEO", "SFTP", "SGML", "SHA", "SID", "SIEM", "SIM", "SIMD",
    "SIMM", "SISD", "SLA", "SLI", "SLOC", "SMB", "SME", "SMP",
    "SMS", "SMT", "SMTP", "SNA", "SNMP", "SOA", "SOAR", "SOC",
    "SOM", "SOP", "SOW", "SPF", "SPI", "SQL", "SRAM", "SRP",
    "SRTP", "SSD", "SSDP", "SSE", "SSH", "SSI", "SSID", "SSL",
    "SSO", "SSP", "SSRF", "SSTP", "STP", "STUN", "SVC", "SVG",
    "SVGA", "SVP", "TACACS", "TAM", "TAPI", "TAR", "TBA", "TBD",
    "TCP", "TDD", "TDE", "TDMA", "TDP", "TFT", "TFTP", "TIFF",
    "TKIP", "TLD", "TLS", "TLV", "TOS", "TOTP", "TPM", "TPU",
    "TSO", "TSP", "TSR", "TTF", "TTL", "TTS", "TTY", "TUI",
    "UAE", "UART", "UAT", "UAV", "UDP", "UEFI", "UEM", "UHF",
    "UI", "UID", "UK", "UML", "UMTS", "UN", "UNC", "UPS",
    "URI", "URL", "URN", "USA", "USB", "UTC", "UTF", "UTM",
    "UTP", "UUCP", "UUID", "UWP", "UX", "V2X", "VAE", "VBA",
    "VBS", "VDI", "VDSL", "VFS", "VGA", "VHD", "VHF", "VLAN",
    "VLF", "VLIW", "VLSI", "VM", "VMM", "VNC", "VOD", "VP",
    "VPC", "VPN", "VPS", "VPU", "VR", "VRAM", "VSAT", "VTL",
    "VUI", "W3C", "WAF", "WAN", "WAP", "WAU", "WAV", "WBS",
    "WCAG", "WCF", "WDM", "WEBM", "WEP", "WFH", "WIP", "WLAN",
    "WMA", "WMI", "WMV", "WPA", "WPS", "WSDL", "WSL", "WWW",
    "WYSIWYG", "XACML", "XAML", "XDR", "XHTML", "XML", "XMPP", "XP",
    "XR", "XSD", "XSL", "XSLT", "XSS", "Y2K", "YACC", "YAGNI",
    "YAML", "ZIF", "ZIP", "ZTNA",
}
ACRONYMS = set(DEFAULT_ACRONYMS)


_INNER_BOUNDARY = set("-_/.")
_URL_RE = re.compile(r"^(https?|ftp|file|mailto):", re.IGNORECASE)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+")
_LEAD_RE = re.compile(r"^([^A-Za-z0-9]+)(.*)$")
_TRAIL_RE = re.compile(r"^(.*?)([^A-Za-z0-9]+)$")


def _split_lead_trail(t: str) -> tuple[str, str, str]:
    if m := _LEAD_RE.match(t):
        lead, core = m.group(1), m.group(2)
    else:
        lead, core = "", t
    if m := _TRAIL_RE.match(core):
        core, trail = m.group(1), m.group(2)
    else:
        trail = ""
    return lead, core, trail


def _title_case_chars(s: str) -> str:
    out: list[str] = []
    up_next = True
    for ch in s:
        if ch in _INNER_BOUNDARY:
            out.append(ch)
            up_next = True
        elif up_next:
            out.append(ch.upper())
            up_next = False
        else:
            out.append(ch.lower())
    return "".join(out)


def _normalize_word(w: str) -> str:
    out: list[str] = []
    seen = False
    for ch in w:
        if ch.isalpha():
            out.append(ch.upper() if not seen else ch.lower())
            seen = True
        else:
            out.append(ch)
    return "".join(out)


def _title_case_token(t: str) -> str:
    lead, core, trail = _split_lead_trail(t)
    if not core:
        return t
    if core.lower() in BRANDS:
        return f"{lead}{BRANDS[core.lower()]}{trail}"
    if core.upper() in ACRONYMS:
        return f"{lead}{core.upper()}{trail}"
    return f"{lead}{_title_case_chars(core)}{trail}"


def _repair_token(t: str) -> str:
    if _URL_RE.match(t):
        return t
    if "@" in t and _EMAIL_RE.search(t):
        return t
    if any(c in t for c in "_/\\"):
        return t

    lead, core, trail = _split_lead_trail(t)
    if not core:
        return t

    if core in ("i", "I"):
        return f"{lead}I{trail}"

    key = core.lower()
    if key in BRANDS:
        return f"{lead}{BRANDS[key]}{trail}"

    if core.isupper() and core.isalpha() and core in ACRONYMS:
        return f"{lead}{core}{trail}"

    if re.fullmatch(r"[a-z0-9]+", core):
        return f"{lead}{core}{trail}"

    return f"{lead}{_normalize_word(core)}{trail}"


def _walk_tokens(s: str, fn: Callable[[str], str]) -> str:
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        j = i
        while j < n and s[j].isspace():
            j += 1
        out.append(s[i:j])
        i = j
        while j < n and not s[j].isspace():
            j += 1
        if j > i:
            out.append(fn(s[i:j]))
        i = j
    return "".join(out)


def to_title(s: str) -> str:
    return _walk_tokens(s, _title_case_token)


def repair(s: str) -> str:
    return _walk_tokens(s, _repair_token)


def toggle_case(s: str) -> str:
    return s.swapcase()


def to_snake(s: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"[\s\-\.]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s.lower()


def to_camel(s: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    parts = [p for p in re.split(r"[\s_\-\.]+", s) if p]
    if not parts:
        return ""
    head, *rest = parts
    return head.lower() + "".join(p[:1].upper() + p[1:].lower() for p in rest)


TRANSFORMS: dict[str, tuple[str, Callable[[str], str]]] = {
    "ctrl+alt+r": ("Repair", repair),
    "ctrl+alt+u": ("UPPER",  str.upper),
    "ctrl+alt+l": ("lower",  str.lower),
    "ctrl+alt+t": ("Title",  to_title),
    "ctrl+alt+k": ("tOGGLE", toggle_case),
    "ctrl+alt+s": ("snake",  to_snake),
    "ctrl+alt+m": ("camel",  to_camel),
}


_SENTINEL = "__TT_SENTINEL__"


def _wait_for_change(initial: str, timeout: float) -> bool:
    import pyperclip
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            current = pyperclip.paste()
        except Exception:
            current = initial
        if current and current != initial:
            return True
        time.sleep(0.02)
    return False


def transform_selection(label: str, fn: Callable[[str], str]) -> None:
    import keyboard
    import pyperclip
    try:
        saved = pyperclip.paste()
    except Exception:
        saved = ""
    pasted = False
    try:
        pyperclip.copy(_SENTINEL)
        keyboard.send("ctrl+c")
        if not _wait_for_change(_SENTINEL, CLIPBOARD_TIMEOUT):
            LOG.info("%s aborted: no text selected", label)
            return
        original = pyperclip.paste()
        if not original or original == _SENTINEL:
            return
        if MAX_LENGTH and len(original) > MAX_LENGTH:
            LOG.info("%s aborted: selection too large (%d)", label, len(original))
            return
        pyperclip.copy(fn(original))
        keyboard.send("ctrl+v")
        pasted = True
        LOG.info("%s applied (%d chars)", label, len(original))
    except Exception:
        LOG.exception("transform_selection failed")
    finally:
        if pasted:
            time.sleep(RESTORE_DELAY)
        try:
            pyperclip.copy(saved)
        except Exception:
            pass


def main() -> int:
    import keyboard

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-5s  %(message)s",
        handlers=[
            logging.FileHandler(Path(__file__).with_name("text_transformer.log"), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    for combo, (label, fn) in TRANSFORMS.items():
        keyboard.add_hotkey(combo, transform_selection, args=(label, fn), suppress=False)
        LOG.info("Bound %s -> %s", combo, label)

    keyboard.add_hotkey("ctrl+shift+esc", lambda: sys.exit(0))
    LOG.info("Ready. Ctrl+Shift+Esc to quit.")
    keyboard.wait()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
