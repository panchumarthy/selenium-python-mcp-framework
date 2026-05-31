# Selenium Python MCP Framework

An AI-powered UI testing framework combining **Selenium**, **Page Object Model**, and the **Model Context Protocol (MCP)**. Claude Code acts as the AI agent — it connects to the local MCP server and drives a real Chrome browser using Selenium tools, with no paid API key required.

## Architecture

```
Interactive AI testing (Claude Code + MCP):

  You (plain-English goal in Claude Code chat)
              ↓
     Claude Code (AI agent — free with your plan)
              ↓  MCP tool calls
     mcp_server/server.py  (local MCP server)
              ↓
     Selenium WebDriver → Chrome → https://www.saucedemo.com

Automated CI testing (pytest + POM, no AI needed):

  pytest → tests/test_saucedemo_pom.py → pages/ (POM) → Selenium → Chrome
```

## Two Testing Modes

| Mode | How | When |
|---|---|---|
| **AI-driven (interactive)** | Claude Code chat + MCP server | Exploratory, self-healing, natural language |
| **POM-based (automated)** | `pytest tests/test_saucedemo_pom.py` | CI/CD, regression, fast feedback |

## Project Structure

```
selenium-python-mcp-framework/
├── mcp_server/
│   ├── server.py          # MCP server — exposes Selenium as tools for Claude Code
│   └── browser_tools.py   # Selenium tool implementations
├── pages/
│   ├── base_page.py       # Base Page Object
│   ├── login_page.py      # SauceDemo login page
│   ├── inventory_page.py  # Products/inventory page
│   └── cart_page.py       # Shopping cart page
├── utils/
│   └── driver_factory.py  # WebDriver factory (shared by MCP server + pytest)
├── tests/
│   └── test_saucedemo_pom.py   # Standard POM-based pytest tests (CI)
├── .mcp.json              # Registers MCP server with Claude Code (auto-loads)
├── test_goals.md          # Plain-English test goals for Claude Code sessions
├── screenshots/           # Auto-saved screenshots
├── .github/workflows/ci.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
└── .env.example
```

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/selenium-python-mcp-framework.git
cd selenium-python-mcp-framework
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run automated POM tests

```bash
# Run all tests
pytest tests/test_saucedemo_pom.py -v

# With HTML report
pytest tests/test_saucedemo_pom.py --html=reports/report.html --self-contained-html

# Headless (no browser window)
HEADLESS=true pytest tests/test_saucedemo_pom.py -v
```

### 3. AI-driven testing with Claude Code

Open this project in Claude Code (CLI or IDE extension). The `.mcp.json` file automatically registers the `selenium-browser` MCP server. Then paste any goal from `test_goals.md` into the chat:

```
Use the selenium-browser MCP tools: log into https://www.saucedemo.com
with standard_user / secret_sauce. Add 2 items to the cart and verify
the badge shows 2. Screenshot: 'test_cart.png'. Report PASS or FAIL.
```

Claude drives the browser, adapts to what it sees, and reports the result.

## MCP Tools Available

| Tool | Description |
|---|---|
| `start_browser` | Launch Chrome (headless optional) |
| `navigate_to` | Go to a URL |
| `get_page_text` | Read all visible text on page |
| `get_page_source` | Get HTML source (first 8000 chars) |
| `find_elements` | Find elements by CSS/XPath/ID/name |
| `click_element` | Click an element |
| `fill_input` | Type into an input field |
| `press_key` | Press enter/tab/escape |
| `get_element_attribute` | Read an HTML attribute |
| `take_screenshot` | Save screenshot to `screenshots/` |
| `get_current_url` | Get current URL and title |
| `wait_for_element` | Wait for element to be visible |
| `stop_browser` | Close the browser |

## Test Coverage (POM tests)

- Login: valid credentials, invalid credentials, locked-out user, empty fields
- Inventory: page loads, product count, prices, sort by price, sort by name
- Cart: add item, add multiple items, remove item, continue shopping
- Checkout: complete end-to-end flow with order confirmation

## Tech Stack

- [Selenium 4](https://selenium-python.readthedocs.io/) — browser automation
- [MCP](https://modelcontextprotocol.io/) — tool protocol connecting Claude Code to Selenium
- [Claude Code](https://claude.ai/code) — AI agent (no separate API key needed)
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) — automatic ChromeDriver
- [pytest](https://pytest.org/) + [pytest-html](https://pytest-html.readthedocs.io/) — test runner + reports
- [SauceDemo](https://www.saucedemo.com/) — demo e-commerce site
