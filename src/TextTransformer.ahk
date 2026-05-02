#Requires AutoHotkey v2.0
#SingleInstance Force

SendMode("Input")
SetKeyDelay(-1, -1)

global CONFIG_FILE := A_ScriptDir "\config.ini"
global LOG_FILE    := A_ScriptDir "\text_transformer.log"
global ENABLED     := true
global Cfg         := Map()
global BRANDS      := Map()
global ACRONYMS    := Map()

LoadConfig()
SetupTray()
RegisterHotkeys()
Log("Started; PID " ProcessExist())
return

LoadConfig() {
    global Cfg, LOG_FILE
    EnsureDefaultConfig()

    Cfg["Repair"] := IniRead(CONFIG_FILE, "Hotkeys", "Repair", "^!r")
    Cfg["Upper"]  := IniRead(CONFIG_FILE, "Hotkeys", "Upper",  "^!u")
    Cfg["Lower"]  := IniRead(CONFIG_FILE, "Hotkeys", "Lower",  "^!l")
    Cfg["Title"]  := IniRead(CONFIG_FILE, "Hotkeys", "Title",  "^!t")
    Cfg["Toggle"] := IniRead(CONFIG_FILE, "Hotkeys", "Toggle", "^!k")
    Cfg["Snake"]  := IniRead(CONFIG_FILE, "Hotkeys", "Snake",  "^!s")
    Cfg["Camel"]  := IniRead(CONFIG_FILE, "Hotkeys", "Camel",  "^!m")

    Cfg["ClipboardTimeout"]  := IniRead(CONFIG_FILE, "Behavior", "ClipboardTimeout", "0.8") + 0
    Cfg["RestoreDelay"]      := IniRead(CONFIG_FILE, "Behavior", "RestoreDelay",     "200") + 0
    Cfg["MaxLength"]         := IniRead(CONFIG_FILE, "Behavior", "MaxLength",        "0")   + 0
    Cfg["ShowNotifications"] := IniRead(CONFIG_FILE, "Behavior", "ShowNotifications", "1") = "1"

    Cfg["LoggingEnabled"]    := IniRead(CONFIG_FILE, "Logging", "Enabled", "1") = "1"
    LOG_FILE                 := A_ScriptDir "\" IniRead(CONFIG_FILE, "Logging", "LogFile", "text_transformer.log")

    LoadBrandList(IniRead(CONFIG_FILE, "Repair", "Brands",    DefaultBrands()))
    LoadAcronymList(IniRead(CONFIG_FILE, "Repair", "Acronyms", DefaultAcronyms()))
}

DefaultBrands() {
    return "iPhone,iPad,iPod,iMac,iCloud,iOS,iPadOS,macOS,watchOS,tvOS,iWork,iMovie,iTunes,iBooks,"
         . "FaceTime,FaceID,TouchID,MacBook,AirPods,AirTag,AirPlay,AirDrop,HomePod,AppleCare,AppleScript,"
         . "PowerPoint,OneDrive,OneNote,SharePoint,PowerShell,PowerBI,PowerToys,IntelliSense,ReSharper,VBScript,JScript,DirectX,"
         . "JavaScript,TypeScript,CoffeeScript,ActionScript,PostScript,LiveScript,"
         . "Node.js,Next.js,Nuxt.js,Vue.js,Three.js,Express.js,Nest.js,jQuery,FastAPI,NestJS,RxJS,"
         . "GraphQL,PostgreSQL,MySQL,NoSQL,MongoDB,MariaDB,DynamoDB,CockroachDB,ElasticSearch,OpenSearch,"
         . "ClickHouse,DuckDB,PlanetScale,Supabase,Firebase,BigQuery,BigTable,RocksDB,SurrealDB,EdgeDB,FaunaDB,"
         . "GitHub,GitLab,BitBucket,GitOps,GitFlow,GitKraken,JetBrains,IntelliJ,PyCharm,WebStorm,"
         . "RubyMine,GoLand,DataGrip,AppCode,TeamCity,SourceTree,NetBeans,"
         . "TensorFlow,PyTorch,OpenCV,OpenAI,ChatGPT,DeepMind,DeepSeek,HuggingFace,MidJourney,"
         . "OpenStack,OpenShift,OpenSSH,OpenSSL,OpenJDK,OpenWRT,OpenLDAP,OpenSUSE,OpenID,"
         . "FreeBSD,OpenBSD,NetBSD,DragonFlyBSD,ChromeOS,ChromeBook,LineageOS,GrapheneOS,"
         . "WordPress,WooCommerce,BigCommerce,SoundCloud,MailChimp,MailGun,FedEx,eBay,GoFundMe,GoDaddy,GoPro,"
         . "DuckDuckGo,MetaMask,ProtonMail,ProtonVPN,DataDog,PagerDuty,HashiCorp,JPMorgan,DreamWorks,ResearchGate,"
         . "DevOps,FinOps,MLOps,DataOps,AIOps,"
         . "PayPal,ApplePay,GooglePay,AmazonPay,SamsungPay,AliPay,"
         . "WhatsApp,LinkedIn,YouTube,TikTok,SnapChat,WeChat,KakaoTalk,"
         . "TeX,LaTeX,BibTeX,XeTeX,LuaTeX,JSDoc,TypeDoc,JavaDoc,"
         . "WebGL,WebRTC,WebAssembly,WebSocket,"
         . "SaaS,PaaS,IaaS,FaaS,OAuth,PhD,MSc,BSc,DALL-E,PlayStation,Bluetooth"
}

DefaultAcronyms() {
    return "2FA,AAA,AAC,ABAC,ABI,ACID,ACK,ACL,ACM,ACPI,ADC,ADO,ADSL,ADT,"
         . "AES,AGI,AGP,AHCI,AI,AMOLED,AMQP,ANSI,AOP,AOT,APFS,API,APK,APU,"
         . "AR,ARGB,ARP,ARPA,ARPANET,ARR,ASAP,ASCII,ASIC,ASLR,ASN,AST,ATA,AUP,"
         . "AV,AVC,AVI,AWT,B2B,B2C,B2E,BBS,BCC,BCD,BCP,BDD,BERT,BFS,"
         . "BGP,BIOS,BMP,BOM,BPM,BSD,BSS,BYOD,CAC,CAD,CAE,CAM,CAPTCHA,CASB,"
         . "CCM,CCTV,CD,CDE,CDMA,CDN,CDP,CEO,CFG,CFO,CGI,CI,CIA,CIDR,"
         . "CIFS,CIM,CIO,CISA,CISC,CISO,CJK,CLI,CMDB,CMM,CMMI,CMO,CMOS,CMS,"
         . "CMYK,CNC,CNN,COB,COBOL,COO,CORBA,CORS,COTS,CPAN,CPU,CRC,CRLF,CRM,"
         . "CRT,CRUD,CS,CSO,CSP,CSR,CSRF,CSS,CSV,CTO,CTR,CV,CVE,CVS,"
         . "CVSS,CX,DAC,DAO,DAS,DAU,DBA,DBMS,DCOM,DDL,DDR,DDoS,DEB,DEP,"
         . "DES,DFS,DHCP,DHTML,DIMM,DIY,DKIM,DLC,DLL,DLP,DMA,DMARC,DMCA,DMG,"
         . "DMI,DML,DMV,DMZ,DNAT,DNS,DOCSIS,DOD,DOJ,DOM,DOS,DPI,DPO,DRAM,"
         . "DRM,DSL,DSN,DSP,DSS,DTD,DTLS,DTO,DVI,DVR,EAP,EBCDIC,EBITDA,EBS,"
         . "EC2,ECC,ECDSA,ECMA,EDA,EDI,EDR,EEPROM,EFI,EFS,EIGRP,EMI,ENIAC,EOD,"
         . "EOF,EOL,EOM,EOW,EPROM,ERD,ERP,ESB,ETA,ETL,ETW,EU,EULA,EV,"
         . "EVP,EXE,FAA,FAQ,FBI,FCC,FDA,FDD,FDDI,FDE,FET,FHS,FIFO,FIPS,"
         . "FLAC,FLOPS,FLV,FOSS,FPGA,FPS,FPU,FQDN,FSB,FSF,FSM,FTC,FTP,FTPS,"
         . "FUD,FYI,GAN,GB,GCC,GCM,GCP,GDB,GDPR,GID,GIF,GIS,GNU,GPG,"
         . "GPGPU,GPL,GPO,GPRS,GPT,GPU,GRE,GSM,GTK,GTM,GUI,GUID,HAL,HBA,"
         . "HCI,HCL,HDD,HDL,HDMI,HEX,HIPAA,HMAC,HMI,HPC,HR,HSL,HSM,HSV,"
         . "HTML,HTTP,HTTPS,IAM,IANA,IBM,ICANN,ICMP,ICS,ICT,ID,IDE,IDS,IEC,"
         . "IEEE,IETF,IGMP,IIS,IMAP,IP,IPA,IPC,IPMI,IPO,IPS,IPSEC,IPTV,IPX,"
         . "IRC,IRQ,IRS,ISA,ISDN,ISO,ISP,ISR,ISV,ITIL,ITU,JBOD,JCL,JDBC,"
         . "JDK,JIT,JMS,JNI,JPEG,JPG,JRE,JS,JSON,JSP,JTAG,JVM,JWE,JWS,"
         . "JWT,KB,KDC,KDE,KDF,KMS,KPI,KVM,LACP,LAMP,LAN,LBA,LCD,LDAP,"
         . "LFI,LGPL,LIFO,LLC,LLM,LOC,LRU,LSB,LSI,LSP,LTE,LTL,LTR,LTS,"
         . "LTV,LUN,LVM,LZW,MAC,MAPI,MAU,MBR,MDM,MDR,MFA,MFT,MIB,MIDI,"
         . "MIME,MIMO,MIPS,MKV,ML,MMC,MMO,MMORPG,MMU,MOSFET,MOTD,MOU,MOV,MP3,"
         . "MP4,MPEG,MPLS,MQTT,MRR,MSA,MSB,MSI,MSP,MSSP,MTBF,MTTF,MTTR,MTU,"
         . "MUA,MVC,MVP,NAC,NAK,NAS,NASA,NAT,NATO,NDA,NDP,NFA,NFC,NFS,"
         . "NGFW,NIC,NIST,NLE,NLG,NLP,NLU,NMI,NNTP,NOC,NOP,NPC,NPU,NSA,"
         . "NTFS,NTLM,NTP,NUMA,NVD,NVMe,NVR,NVRAM,OCR,OCSP,ODBC,OEM,OFDM,OGG,"
         . "OID,OKR,OLA,OLAP,OLE,OLED,OLTP,OOM,OOP,OOTB,ORM,OS,OSI,OSINT,"
         . "OSPF,OTP,OUI,OWASP,P2P,PAM,PBX,PC,PCB,PCI,PCIe,PCM,PCRE,PDA,"
         . "PDF,PEM,PFS,PGP,PHI,PHP,PID,PII,PKCS,PKI,PLC,PNG,POP3,POSIX,"
         . "PPP,PPTP,PR,PRNG,PSK,PSTN,PSU,PTO,PXE,QA,QC,QEMU,QR,RAG,"
         . "RAID,RAII,RAM,RARP,RBAC,RCA,RDBMS,RDP,RDS,RFB,RFC,RFI,RFID,RFP,"
         . "RFQ,RGB,RGBA,RISC,RLHF,RMI,RNN,ROI,ROM,RPA,RPC,RPG,RPM,RPO,"
         . "RSA,RSI,RSS,RST,RSVP,RTC,RTL,RTOS,RTP,RTSP,RTT,RWD,SAML,SAS,"
         . "SASE,SASL,SATA,SCADA,SCCM,SCM,SCP,SCSI,SCSS,SDK,SDLC,SDN,SDR,SDRAM,"
         . "SEO,SFTP,SGML,SHA,SID,SIEM,SIM,SIMD,SIMM,SISD,SLA,SLI,SLOC,SMB,"
         . "SME,SMP,SMS,SMT,SMTP,SNA,SNMP,SOA,SOAR,SOC,SOM,SOP,SOW,SPF,"
         . "SPI,SQL,SRAM,SRP,SRTP,SSD,SSDP,SSE,SSH,SSI,SSID,SSL,SSO,SSP,"
         . "SSRF,SSTP,STP,STUN,SVC,SVG,SVGA,SVP,TACACS,TAM,TAPI,TAR,TBA,TBD,"
         . "TCP,TDD,TDE,TDMA,TDP,TFT,TFTP,TIFF,TKIP,TLD,TLS,TLV,TOS,TOTP,"
         . "TPM,TPU,TSO,TSP,TSR,TTF,TTL,TTS,TTY,TUI,UAE,UART,UAT,UAV,"
         . "UDP,UEFI,UEM,UHF,UI,UID,UK,UML,UMTS,UN,UNC,UPS,URI,URL,"
         . "URN,USA,USB,UTC,UTF,UTM,UTP,UUCP,UUID,UWP,UX,V2X,VAE,VBA,"
         . "VBS,VDI,VDSL,VFS,VGA,VHD,VHF,VLAN,VLF,VLIW,VLSI,VM,VMM,VNC,"
         . "VOD,VP,VPC,VPN,VPS,VPU,VR,VRAM,VSAT,VTL,VUI,W3C,WAF,WAN,"
         . "WAP,WAU,WAV,WBS,WCAG,WCF,WDM,WEBM,WEP,WFH,WIP,WLAN,WMA,WMI,"
         . "WMV,WPA,WPS,WSDL,WSL,WWW,WYSIWYG,XACML,XAML,XDR,XHTML,XML,XMPP,XP,"
         . "XR,XSD,XSL,XSLT,XSS,Y2K,YACC,YAGNI,YAML,ZIF,ZIP,ZTNA"
}

LoadBrandList(csv) {
    global BRANDS
    BRANDS := Map()
    for entry in StrSplit(csv, ",") {
        e := Trim(entry)
        if e != ""
            BRANDS[StrLower(e)] := e
    }
}

LoadAcronymList(csv) {
    global ACRONYMS
    ACRONYMS := Map()
    for entry in StrSplit(csv, ",") {
        e := Trim(entry)
        if e != ""
            ACRONYMS[e] := true
    }
}

EnsureDefaultConfig() {
    if FileExist(CONFIG_FILE)
        return
    header := "
    (
[Hotkeys]
; ^=Ctrl  +=Shift  !=Alt  #=Win
; AltGr keyboards: swap Ctrl+Alt for Win+Shift (e.g. #+r).
Repair=^!r
Upper=^!u
Lower=^!l
Title=^!t
Toggle=^!k
Snake=^!s
Camel=^!m

[Behavior]
ClipboardTimeout=0.8
RestoreDelay=200
MaxLength=0
ShowNotifications=1

[Logging]
Enabled=1
LogFile=text_transformer.log

[Repair]
; Don't add words that are also common English (IS, IT, AS, REST...) -
; they'd corrupt Title Case ("the data is hot" -> "The Data IS Hot").
    )"
    body := header "`r`nBrands=" DefaultBrands() "`r`nAcronyms=" DefaultAcronyms() "`r`n"
    FileAppend(body, CONFIG_FILE, "UTF-8")
}

RegisterHotkeys() {
    SafeBind(Cfg["Repair"], (*) => TransformSelection(Repair,      "Repair"))
    SafeBind(Cfg["Upper"],  (*) => TransformSelection(StrUpper,    "UPPER"))
    SafeBind(Cfg["Lower"],  (*) => TransformSelection(StrLower,    "lower"))
    SafeBind(Cfg["Title"],  (*) => TransformSelection(ToTitleCase, "Title"))
    SafeBind(Cfg["Toggle"], (*) => TransformSelection(ToggleCase,  "tOGGLE"))
    SafeBind(Cfg["Snake"],  (*) => TransformSelection(ToSnakeCase, "snake"))
    SafeBind(Cfg["Camel"],  (*) => TransformSelection(ToCamelCase, "camel"))
}

SafeBind(keyCombo, fn) {
    try {
        Hotkey(keyCombo, fn, "On")
    } catch as err {
        Log("Failed to bind '" keyCombo "': " err.Message)
        Notify("Bad hotkey '" keyCombo "' - check config.ini")
    }
}

TransformSelection(transformFn, label) {
    static busy := false

    if !ENABLED {
        Notify("Disabled - re-enable from the tray icon")
        return
    }
    if busy
        return
    busy := true
    pasted := false

    savedClip := ClipboardAll()
    try {
        A_Clipboard := ""
        Send("^c")
        ; ClipWait mode 0: wait for text only, so empty selections and image
        ; selections both fall through to the timeout branch.
        if !ClipWait(Cfg["ClipboardTimeout"], 0) {
            Notify("No text selected")
            Log(label " aborted: clipboard empty or non-text")
            return
        }

        original := A_Clipboard
        if (original = "") {
            Notify("Empty selection")
            return
        }
        if (Cfg["MaxLength"] > 0 && StrLen(original) > Cfg["MaxLength"]) {
            Notify("Selection too large (" StrLen(original) " chars)")
            Log(label " aborted: exceeds MaxLength")
            return
        }

        transformed := transformFn(original)

        A_Clipboard := transformed
        if !ClipWait(0.5, 1) {
            Notify("Clipboard write failed")
            return
        }
        Send("^v")
        pasted := true
        Log(label " applied (" StrLen(original) " chars)")
    } catch as err {
        Log("Exception: " err.Message)
        Notify("Error: " err.Message)
    } finally {
        if pasted
            Sleep(Cfg["RestoreDelay"])
        A_Clipboard := savedClip
        savedClip := ""
        busy := false
    }
}

ToTitleCase(s) {
    out := ""
    pos := 1
    n := StrLen(s)
    while pos <= n {
        ws := ""
        while pos <= n {
            ch := SubStr(s, pos, 1)
            if !RegExMatch(ch, "\s")
                break
            ws .= ch
            pos++
        }
        out .= ws
        tok := ""
        while pos <= n {
            ch := SubStr(s, pos, 1)
            if RegExMatch(ch, "\s")
                break
            tok .= ch
            pos++
        }
        if tok != ""
            out .= TitleCaseToken(tok)
    }
    return out
}

TitleCaseToken(t) {
    global BRANDS, ACRONYMS

    lead := ""
    trail := ""
    core := t
    if RegExMatch(core, "^([^A-Za-z0-9]+)(.*)$", &m)
        lead := m[1], core := m[2]
    if RegExMatch(core, "^(.*?)([^A-Za-z0-9]+)$", &m)
        core := m[1], trail := m[2]
    if (core = "")
        return t

    if BRANDS.Has(StrLower(core))
        return lead BRANDS[StrLower(core)] trail

    if ACRONYMS.Has(StrUpper(core))
        return lead StrUpper(core) trail

    return lead TitleCaseChars(core) trail
}

TitleCaseChars(s) {
    out := ""
    upNext := true
    Loop Parse, s {
        ch := A_LoopField
        if RegExMatch(ch, "[\-_/.]") {
            out .= ch
            upNext := true
        } else if upNext {
            out .= StrUpper(ch)
            upNext := false
        } else {
            out .= StrLower(ch)
        }
    }
    return out
}

ToggleCase(s) {
    out := ""
    Loop Parse, s {
        ch := A_LoopField
        if RegExMatch(ch, "[A-Z]")
            out .= StrLower(ch)
        else if RegExMatch(ch, "[a-z]")
            out .= StrUpper(ch)
        else
            out .= ch
    }
    return out
}

ToSnakeCase(s) {
    s := RegExReplace(s, "([a-z0-9])([A-Z])", "$1_$2")
    s := RegExReplace(s, "[\s\-\.]+", "_")
    s := RegExReplace(s, "_+", "_")
    s := Trim(s, "_")
    return StrLower(s)
}

ToCamelCase(s) {
    s := RegExReplace(s, "([a-z0-9])([A-Z])", "$1 $2")
    s := RegExReplace(s, "[_\-\.]+", " ")
    parts := StrSplit(s, A_Space)
    out := ""
    first := true
    for part in parts {
        if (part = "")
            continue
        if first {
            out .= StrLower(part)
            first := false
        } else {
            out .= StrUpper(SubStr(part, 1, 1)) StrLower(SubStr(part, 2))
        }
    }
    return out
}

Repair(s) {
    out := ""
    pos := 1
    n := StrLen(s)
    while pos <= n {
        ws := ""
        while pos <= n {
            ch := SubStr(s, pos, 1)
            if !RegExMatch(ch, "\s")
                break
            ws .= ch
            pos++
        }
        out .= ws

        tok := ""
        while pos <= n {
            ch := SubStr(s, pos, 1)
            if RegExMatch(ch, "\s")
                break
            tok .= ch
            pos++
        }
        if tok != ""
            out .= RepairToken(tok)
    }
    return out
}

RepairToken(t) {
    global BRANDS, ACRONYMS

    if RegExMatch(t, "i)^(https?|ftp|file|mailto):")
        return t
    if InStr(t, "@") && RegExMatch(t, "[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+")
        return t
    if RegExMatch(t, "[_/\\]")
        return t

    lead := ""
    trail := ""
    core := t
    if RegExMatch(core, "^([^A-Za-z0-9]+)(.*)$", &m)
        lead := m[1], core := m[2]
    if RegExMatch(core, "^(.*?)([^A-Za-z0-9]+)$", &m)
        core := m[1], trail := m[2]
    if (core = "")
        return t

    if (core = "i" || core = "I")
        return lead "I" trail

    key := StrLower(core)
    if BRANDS.Has(key)
        return lead BRANDS[key] trail

    if RegExMatch(core, "^[A-Z]+$") && ACRONYMS.Has(core)
        return lead core trail

    if RegExMatch(core, "^[a-z0-9]+$")
        return lead core trail

    return lead NormalizeWord(core) trail
}

NormalizeWord(w) {
    out := ""
    seenLetter := false
    Loop Parse, w {
        ch := A_LoopField
        if RegExMatch(ch, "[A-Za-z]") {
            if !seenLetter {
                out .= StrUpper(ch)
                seenLetter := true
            } else {
                out .= StrLower(ch)
            }
        } else {
            out .= ch
        }
    }
    return out
}

SetupTray() {
    A_IconTip := "Text Transformer"
    tm := A_TrayMenu
    tm.Delete()
    tm.Add("Text Transformer", (*) => 0)
    tm.Disable("Text Transformer")
    tm.Add()
    tm.Add("Enabled", ToggleEnabled)
    tm.Check("Enabled")
    tm.Add("Edit config",   (*) => Run('notepad.exe "' CONFIG_FILE '"'))
    tm.Add("Reload config", (*) => Reload())
    tm.Add("Open log",      (*) => OpenLog())
    tm.Add()
    tm.Add("Exit", (*) => ExitApp())
    tm.Default := "Enabled"
    try TraySetIcon("imageres.dll", 110)
}

ToggleEnabled(itemName, *) {
    global ENABLED
    ENABLED := !ENABLED
    if ENABLED {
        A_TrayMenu.Check(itemName)
        Notify("Hotkeys enabled")
    } else {
        A_TrayMenu.Uncheck(itemName)
        Notify("Hotkeys disabled")
    }
    Log("ENABLED=" (ENABLED ? "true" : "false"))
}

OpenLog() {
    if FileExist(LOG_FILE)
        Run('notepad.exe "' LOG_FILE '"')
    else
        Notify("No log file yet")
}

Notify(text) {
    if !Cfg["ShowNotifications"]
        return
    ToolTip(text)
    SetTimer(() => ToolTip(), -1500)
}

Log(line) {
    if !Cfg["LoggingEnabled"]
        return
    try {
        FileAppend(FormatTime(, "yyyy-MM-dd HH:mm:ss") "  " line "`r`n",
                   LOG_FILE, "UTF-8")
    } catch {
    }
}
