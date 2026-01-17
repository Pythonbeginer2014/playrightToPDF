import asyncio
import logging

from playwright.async_api import async_playwright
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Special classes like .title, .url, .date, .pageNumber, .totalPages inject dynamic values
custom_header_template = """
            <div style="font-size: 10px; width: 100%; text-align: center;">
                <div style="margin-bottom: 5px;">
                <span class="title" style="font-weight: bold;"></span>
                <span class="url" style="color: #666;"></span>
                </div>
                
                <div style="text-align: center; width: 100%; margin-top: 10px; margin-bottom: 10px;">
                 <hr style="border: 0.5px solid #ccc; margin: 5px 0;width:96%;margin: auto;">
                </div>
            </div>
            
        """

# Define a simple footer
custom_footer_template = """
            <div style="font-size: 10px; color: #666; text-align: center; width: 100%; margin-bottom: 10px;">
                Page <span class="pageNumber"></span> of <span class="totalPages"></span>
            </div>
        """

async def url_to_pdf(url: str, output_path: str):
    """
    Navigates to a URL and saves the rendered content as a PDF.
    """

    async with async_playwright() as p:
        # Launch a headless Chromium browser instance
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport=None)

        try:
            logging.info(f"Navigating to {url}...")
            # Navigate to the specified URL
            await page.goto(url, wait_until="networkidle")  # Wait for network to be idle
            logging.info(f"Successfully navigated to {url}")

            # Generate a PDF of the page and save it
            await page.pdf(path=output_path, format="Letter",
                           display_header_footer=True,  # Must be True to show header/footer
                           header_template=custom_header_template,
                           footer_template=custom_footer_template,
                           margin={"top": "50px",
                                   "right": "35px",
                                   "bottom": "50px",
                                   "left": "35px"},

                           print_background=False,
                           scale=1.0,
                           )  # Customize PDF options
            logging.info(f"PDF saved to {output_path}")

        except Exception as e:
            logging.error(f"An error occurred while converting {url} to PDF: {e}")
        finally:
            # Ensure the browser is closed
            await browser.close()


async def generate_pdf_from_html(html_content, output_path="output.pdf"):
    """
    Converts a raw HTML string into a PDF file using Playwright.
    """
    async with async_playwright() as p:
        # Launch a headless Chromium browser instance
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Set the page content to the provided HTML string
        await page.set_content(html_content)

        # Generate the PDF and save it to the specified path
        # Note: PDF generation is currently only supported in headless Chromium
        await page.pdf(path=output_path)

        # Close the browser
        await browser.close()
        print(f"PDF successfully generated at {output_path}")


if __name__ == "__main__":
    asyncio.run(url_to_pdf("http://www.godyabo.com/zhurijiangzhang/46875.html", "playwright.pdf"))
