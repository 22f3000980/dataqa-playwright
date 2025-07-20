from playwright.sync_api import sync_playwright
import re

seeds = range(61, 71)
total = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for seed in seeds:
        url = f"https://exam-data.vercel.app/{seed}"
        page.goto(url)
        page.wait_for_timeout(1000)  # wait for tables to load

        # Get all numbers in all tables
        numbers = page.eval_on_selector_all("table", """
            elements => elements.flatMap(table =>
                Array.from(table.querySelectorAll('td')).map(cell => cell.textContent)
            )
        """)
        # Convert and sum
        page_total = sum(
            int(re.sub(r"[^\d]", "", n)) for n in numbers if re.sub(r"[^\d]", "", n).isdigit()
        )
        print(f"Seed {seed} Total: {page_total}")
        total += page_total

    print(f"\nFinal Total Across All Pages: {total}")
    browser.close()
