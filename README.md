# Hermes Sales Agent - 🧠 Intelligent Lead Orchestrator

An **AI-powered Telegram sales agent** with an intelligent orchestrator that decides which services to call, in what order, for optimal lead processing.

## 🎯 Key Feature: Intelligent Orchestrator

The **Hermes Orchestrator** is the "brain" of the system:

```
Orchestrator Agent
├── 📊 Analyzes lead data
├── 🤔 Makes strategic decisions
│   ├── Research First Strategy
│   ├── Score Only Strategy
│   ├── Score & Outreach Strategy
│   └── Bulk Campaign Strategy
├── 🎯 Decides tool usage (which service to call)
├── 🔄 Calls appropriate services in sequence
│   ├── Research Service (if needed)
│   ├── Scoring Service (always)
│   ├── Outreach Service (if qualified)
│   └── Report Service (on demand)
├── 📈 Determines lead priority
│   ├── CRITICAL (80+)
│   ├── HIGH (60-80)
│   ├── MEDIUM (30-60)
│   └── LOW (<30)
└── 📋 Formats final response
```

## ✨ Features

### 🤖 Intelligent Decision Making
- **Analyzes** incoming lead data
- **Determines** optimal processing strategy
- **Selects** which services to invoke
- **Sequences** service calls intelligently
- **Prioritizes** leads by score and potential

### 🔧 Multi-Strategy Processing
1. **Research First** - Gathers company data before scoring
2. **Score Only** - Evaluates lead without outreach
3. **Score & Outreach** - Full pipeline with message generation
4. **Bulk Campaign** - Processes multiple leads simultaneously

### 🎯 Lead Prioritization
- **CRITICAL** (80+) - Immediate action needed
- **HIGH** (60-80) - Quick follow-up
- **MEDIUM** (30-60) - Standard processing
- **LOW** (<30) - Queue for later

### 🧠 AI-Powered Features
- Generate personalized outreach messages
- Create compelling email subject lines
- Score leads based on multiple factors
- Intelligent lead research

### 💾 Chroma Cloud Integration
- Vector database for lead storage
- Semantic search capabilities
- Scalable cloud infrastructure
- Embeddings support

### 📊 Real-time Analytics
- Campaign performance tracking
- Conversion metrics
- Lead statistics
- Custom reporting

## 📋 Technology Stack

- **Bot Framework**: `python-telegram-bot`
- **Vector DB**: Chroma Cloud (remote)
- **AI Models**: Google Gemini + NVIDIA
- **Language**: Python 3.9+
- **Architecture**: Microservices with intelligent orchestration

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/akshat2685/sales_agent.git
cd sales_agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Running the Bot

```bash
python main.py
```

## 📱 Telegram Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | - | Initialize bot & show welcome |
| `/help` | - | Show all available commands |
| `/add_lead` | `<first> <last> <email> [company]` | Add new lead with orchestrator processing |
| `/list_leads` | - | View recent leads |
| `/search_leads` | `<query>` | Search leads by name/company |
| `/analytics` | - | Get campaign analytics & metrics |
| `/campaign` | `[count]` | Run bulk campaign (default: 3 leads) |

### Examples

```
/add_lead John Doe john@techcorp.com "TechCorp Inc"
/search_leads TechCorp
/campaign 5
/analytics
```

## 🧠 How the Orchestrator Works

### Processing Flow

```
User Input (Telegram)
    ↓
[Orchestrator.process_lead()]
    ├─ Step 1: Analyze lead data
    │   └─ Check: company, email, title, etc.
    │
    ├─ Step 2: Decide strategy
    │   ├─ Missing company? → RESEARCH_FIRST
    │   ├─ Incomplete data? → SCORE_ONLY
    │   └─ Full data? → SCORE_AND_OUTREACH
    │
    ├─ Step 3: Create lead in database
    │   └─ Store in Chroma Cloud
    │
    └─ Step 4: Execute strategy
        ├─ Call Research Service (if needed)
        ├─ Call Scoring Service
        ├─ Call Outreach Service (if qualified)
        └─ Format response
    
User Response (Telegram)
```

### Decision Logic

**Strategy: RESEARCH_FIRST**
- Used when: Company info missing
- Calls: Research → Scoring
- Output: Research insights + lead score

**Strategy: SCORE_ONLY**
- Used when: Insufficient data for outreach
- Calls: Scoring
- Output: Lead score + priority

**Strategy: SCORE_AND_OUTREACH**
- Used when: Complete lead information
- Calls: Scoring → Research → Outreach
- Output: Score + Personalized message + Subject line

**Strategy: BULK_PROCESS**
- Used when: Multiple leads provided
- Calls: Orchestrator.process_lead() for each
- Output: Campaign summary + priority breakdown

## 📊 Example Orchestrator Response

```
╔════════════════════════════════════════╗
║  HERMES ORCHESTRATOR RESPONSE         ║
╚════════════════════════════════════════╝

📊 Status: READY_TO_SEND
🎯 Strategy: SCORE_AND_OUTREACH
🔧 Services Called: scoring_service, research_service, outreach_service

─── LEAD DATA ───
Name: John Doe
Email: john@techcorp.com
Company: TechCorp Inc

─── ANALYSIS DATA ───
Score: 75.50/100
Priority: HIGH
Reason: Strong match for outreach

─── OUTREACH MESSAGE ───
Hi John,

I've been impressed by TechCorp's recent innovations...
[AI-generated personalized message]

─── EMAIL SUBJECT ───
Collaboration Opportunity at TechCorp
```

## 🏗️ Project Structure

```
app/
├── agent/
│   └── orchestrator.py          ← THE BRAIN (decision logic)
├── bot/
│   └── telegram_handlers.py     ← Bot commands
├── services/
│   ├── lead_service.py          ← Lead management
│   ├── scoring_service.py       ← Lead scoring
│   ├── outreach_service.py      ← Message generation
│   ├── research_service.py      ← Company research
│   └── report_service.py        ← Analytics
├── database/
│   ├── chroma_client.py         ← Chroma Cloud client
│   └── models.py                ← Data models
├── config/
│   └── settings.py              ← Configuration
└── utils/
    ├── ai_client.py             ← AI models (Gemini/NVIDIA)
    ├── logger.py                ← Logging
    ├── helpers.py               ← Utilities
    └── validators.py            ← Validation

main.py                           ← Entry point
requirements.txt                  ← Dependencies
.env                              ← Configuration (keep secure!)
```

## 🔐 Environment Setup

Create `.env` with your credentials:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Chroma Cloud
CHROMA_HOST=api.trychroma.com
CHROMA_API_KEY=your_api_key
CHROMA_TENANT=your_tenant_id
CHROMA_DATABASE=sales_agent_lead

# AI Models
GEMINI_API_KEY=your_gemini_key
NVIDIA_API_KEY=your_nvidia_key
MODEL_CHOICE=gemini              # or "nvidia"

# App
DEBUG=False
LOG_LEVEL=INFO
```

## 📈 Features in Depth

### Scoring Algorithm
- Company presence: +10 points
- Valid email: +15 points
- Contact history: +20 points
- Qualification status: +40 points
- Conversion: +100 points

### Lead Priority Levels
Based on orchestrator analysis:
- **CRITICAL** 🔴 - Immediate outreach
- **HIGH** 🟠 - Next priority
- **MEDIUM** 🟡 - Standard queue
- **LOW** ⚪ - Future prospects

### Message Generation
- Uses Google Gemini or NVIDIA AI
- Personalizes based on company
- Generates compelling subject lines
- Adapts tone (professional/casual)

## 🚦 Development

### Code Quality
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/
```

### Testing
```bash
pytest
```

## 🛣️ Roadmap

- [ ] Email campaign integration
- [ ] LinkedIn automation
- [ ] Advanced lead enrichment
- [ ] CRM integrations (HubSpot, Salesforce)
- [ ] Web dashboard
- [ ] Multi-user support
- [ ] Advanced analytics

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review example commands

## 📄 License

MIT License - Free for personal and commercial use

---

**Made with ❤️ by Akshat**
