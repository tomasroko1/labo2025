const { chromium } = require('playwright');
const { Client } = require('@notionhq/client');

// Log environment variables for debugging (remove sensitive data in production)
console.log('Environment check:');
console.log('NOTION_TOKEN exists:', !!process.env.NOTION_TOKEN);
console.log('NOTION_TOKEN length:', process.env.NOTION_TOKEN ? process.env.NOTION_TOKEN.length : 0);
console.log('NOTION_DATABASE_ID exists:', !!process.env.NOTION_DATABASE_ID);

if (!process.env.NOTION_TOKEN) {
    console.error('ERROR: NOTION_TOKEN is not set!');
    process.exit(1);
}

if (!process.env.NOTION_DATABASE_ID) {
    console.error('ERROR: NOTION_DATABASE_ID is not set!');
    process.exit(1);
}

const notion = new Client({ auth: process.env.NOTION_TOKEN });
const databaseId = process.env.NOTION_DATABASE_ID;
const SEARCH_URL = 'https://www.linkedin.com/jobs/search/?currentJobId=4361188587&f_JT=P%2CI&f_PP=103813819&geoId=92000000&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=25';

// Helper to get existing job links from Notion
async function getExistingJobLinksFromNotion() {
    const links = new Set();
    let cursor = undefined;

    try {
        while (true) {
            const response = await notion.databases.query({
                database_id: databaseId,
                filter: {
                    property: 'Link',
                    url: {
                        is_not_empty: true,
                    },
                },
                page_size: 100,
                start_cursor: cursor,
            });

            for (const page of response.results) {
                if (page.properties.Link && page.properties.Link.url) {
                    links.add(page.properties.Link.url.split('?')[0]);
                }
            }

            if (!response.has_more) {
                break;
            }
            cursor = response.next_cursor;
        }
    } catch (error) {
        console.error('Error querying Notion database:', error.message);
        console.error('Database ID:', databaseId);
        throw error;
    }
    
    return links;
}

// Helper: Sync to Notion
async function syncJobToNotion(job) {
    try {
        await notion.pages.create({
            parent: { database_id: databaseId },
            properties: {
                'Title': { title: [{ text: { content: job.title } }] },
                'Company': { rich_text: [{ text: { content: job.company } }] },
                'Location': { rich_text: [{ text: { content: job.location } }] },
                'Link': { url: job.link },
                'DateScanned': { date: { start: job.date } },
                'Type': { select: { name: job.type.substring(0, 100) || 'Unknown' } },
                'TechStack': {
                    multi_select: job.stack.split(',')
                        .map(s => s.trim())
                        .filter(s => s.length > 0)
                        .map(s => ({ name: s.replace(/,/g, '').substring(0, 100) }))
                },
                'Summary': { rich_text: [{ text: { content: job.summary.substring(0, 2000) } }] }
            }
        });
        console.log(`Synced to Notion: ${job.title}`);
    } catch (error) {
        console.error(`Failed to sync to Notion: ${error.message}`);
    }
}

(async () => {
    console.log('Launching browser...');
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        console.log('Navigating to job list...');
        await page.goto(SEARCH_URL, { timeout: 60000 });
        await page.waitForTimeout(5000);

        // Scroll to load job list
        console.log('Scrolling to load jobs...');
        for (let i = 0; i < 5; i++) {
            await page.evaluate(() => window.scrollBy(0, 500));
            await page.waitForTimeout(1000);
        }

        // Extract job links from the list
        const jobLinks = await page.evaluate(() => {
            const cards = document.querySelectorAll('.job-card-container, .jobs-search-results__list-item');
            const links = [];
            cards.forEach(card => {
                const titleLink = card.querySelector('a.job-card-list__title--link');
                if (titleLink) {
                    const href = titleLink.href.split('?')[0];
                    links.push(href.startsWith('http') ? href : 'https://www.linkedin.com' + href);
                }
            });
            return links;
        });

        console.log(`Found ${jobLinks.length} potential jobs.`);
        
        if (jobLinks.length === 0) {
            console.log('No jobs found. This might be due to LinkedIn blocking automated access.');
            await browser.close();
            return;
        }
        
        const existingLinks = await getExistingJobLinksFromNotion();

        // Filter out existing
        const newLinks = jobLinks.filter(link => !existingLinks.has(link));
        console.log(`${newLinks.length} are new.`);

        // Process first 15 *new* jobs
        const jobsToProcess = newLinks.slice(0, 15);

        for (const link of jobsToProcess) {
            console.log(`Processing: ${link}`);
            try {
                await page.goto(link, { timeout: 60000 });
                await page.waitForTimeout(3000);

                // Click 'See more' if needed
                const seeMoreButton = await page.$('button[aria-label="See more"], button.jobs-description__footer-button');
                if (seeMoreButton) await seeMoreButton.click().catch(() => { });

                // Extract Details
                const details = await page.evaluate(() => {
                    const title = document.querySelector('h1')?.innerText.trim() || 'Unknown Title';
                    const company = document.querySelector('.job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name')?.innerText.trim() || 'Unknown Company';
                    const location = document.querySelector('.job-details-jobs-unified-top-card__bullet, .jobs-unified-top-card__bullet')?.innerText.trim() || 'Unknown Location';
                    const description = document.querySelector('#job-details, .jobs-description')?.innerText || '';

                    // Simple keyword extraction
                    const type = description.toLowerCase().includes('intern') || description.toLowerCase().includes('pasant') ? 'Internship' : 'Full-time';
                    const stackKeywords = ['python', 'sql', 'excel', 'aws', 'java', 'react', 'node', 'power bi', 'tableau'];
                    const stack = stackKeywords.filter(k => description.toLowerCase().includes(k)).map(k => k.charAt(0).toUpperCase() + k.slice(1)).join(', ');

                    const summary = description.substring(0, 150).replace(/\n/g, ' ') + '...';

                    return { title, company, location, type, stack, summary };
                });

                const jobData = {
                    date: new Date().toISOString().split('T')[0],
                    ...details,
                    link: link
                };

                // Save Immediately
                await syncJobToNotion(jobData);

                // Random delay to be polite
                const delay = Math.floor(Math.random() * 3000) + 2000;
                await page.waitForTimeout(delay);

            } catch (err) {
                console.error(`Error filtering/processing job ${link}: ${err.message}`);
            }
        }

    } catch (error) {
        console.error('Fatal error during scan:', error);
    } finally {
        await browser.close();
    }
})();
