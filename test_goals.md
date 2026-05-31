# AI Agent Test Goals (Claude Code + MCP)

This file contains test goals for interactive AI-driven testing via Claude Code.
Claude Code connects to the MCP server (`.mcp.json`) and drives the browser using
Selenium tools — no API key or extra cost needed.

## How to run

1. Open this project in Claude Code (the CLI or IDE extension)
2. The `selenium-browser` MCP server auto-registers from `.mcp.json`
3. Paste any goal below into the Claude Code chat
4. Claude calls the Selenium tools and reports PASS/FAIL

---

## Login Tests

**Goal 1 — Valid login**
```
Use the selenium-browser MCP tools to test login on SauceDemo:
Navigate to https://www.saucedemo.com, log in with username 'standard_user'
and password 'secret_sauce'. Confirm the inventory page loads after login.
Take a screenshot named 'test_login_pass.png'. Report PASS or FAIL.
```

**Goal 2 — Invalid credentials**
```
Use the selenium-browser MCP tools: navigate to https://www.saucedemo.com,
attempt login with username 'bad_user' and password 'bad_pass'.
Confirm an error message appears. Take a screenshot named 'test_login_fail.png'.
Report PASS if error message is shown, FAIL otherwise.
```

**Goal 3 — Locked out user**
```
Use the selenium-browser MCP tools: go to https://www.saucedemo.com,
try logging in with username 'locked_out_user' and password 'secret_sauce'.
Verify the error message mentions the account is locked out.
Screenshot: 'test_locked_out.png'. Report PASS or FAIL.
```

---

## Shopping Cart Tests

**Goal 4 — Add item to cart**
```
Use the selenium-browser MCP tools: log into https://www.saucedemo.com
with standard_user / secret_sauce. Add the first product to the cart.
Verify the cart badge shows 1. Screenshot: 'test_add_to_cart.png'. Report PASS or FAIL.
```

**Goal 5 — Add two specific items**
```
Use the selenium-browser MCP tools: log into SauceDemo (standard_user / secret_sauce).
Add 'Sauce Labs Backpack' and 'Sauce Labs Bike Light' to the cart.
Verify the cart badge shows 2. Screenshot: 'test_two_items.png'. Report PASS or FAIL.
```

**Goal 6 — Remove item from cart**
```
Use the selenium-browser MCP tools: log into SauceDemo (standard_user / secret_sauce).
Add any product to the cart. Navigate to the cart. Remove the item.
Verify the cart is now empty. Screenshot: 'test_cart_empty.png'. Report PASS or FAIL.
```

---

## Inventory Tests

**Goal 7 — Sort by price**
```
Use the selenium-browser MCP tools: log into SauceDemo (standard_user / secret_sauce).
Sort the products by 'Price (low to high)'. Read the first two product prices and
confirm the first is cheaper than or equal to the second.
Screenshot: 'test_sort_price.png'. Report PASS or FAIL.
```

**Goal 8 — Product count**
```
Use the selenium-browser MCP tools: log into SauceDemo (standard_user / secret_sauce).
Count the products on the inventory page. Confirm there are exactly 6.
Screenshot: 'test_product_count.png'. Report PASS or FAIL.
```

---

## End-to-End Tests

**Goal 9 — Full checkout**
```
Use the selenium-browser MCP tools to complete a full checkout on SauceDemo:
1. Navigate to https://www.saucedemo.com and log in (standard_user / secret_sauce)
2. Add any one product to the cart
3. Open the cart and click Checkout
4. Fill in: First Name=John, Last Name=Doe, Zip=12345
5. Click Continue, then Finish
6. Verify an order confirmation message appears
Screenshot: 'test_checkout_complete.png'. Report PASS or FAIL.
```
