const { Client } = require('@notionhq/client');
require('dotenv').config();
const fs = require('fs');
const path = require('path');

const notion = new Client({ auth: process.env.NOTION_TOKEN });
const databaseId = process.env.NOTION_DATABASE_ID;
const jobsFilePath = process.argv[2] ? path.resolve(process.argv[2]) : path.join(__dirname, '../jobs.md');

// Helper to parse the markdown table
function parseJobsFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    const jobs = [];

    // Find the table start
    let tableStart = -1;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('| Date | Title |')) {
            tableStart = i;
            break;
        }
    }

    if (tableStart === -1) return [];

    // Skip header and separator
    for (let i = tableStart + 2; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line.startsWith('|')) continue;

        const parts = line.split('|').map(p => p.trim()).filter(p => p !== '');
        if (parts.length < 8) continue; // Ensure we have enough columns

        // Extract Link URL from markdown [Link](url)
        const linkMatch = parts[7].match(/\((.*?)\)/);
        const linkUrl = linkMatch ? linkMatch[1] : parts[7];

        jobs.push({
            date: parts[0],
            title: parts[1],
            company: parts[2],
            location: parts[3],
            type: parts[4],
            stack: parts[5],
            summary: parts[6],
            link: linkUrl
        });
    }
    return jobs;
}

// Convert "YYYY-MM-DD" to ISO 8601 for Notion
function formatDate(dateStr) {
    try {
        const date = new Date(dateStr);
        return date.toISOString().split('T')[0]; // Return YYYY-MM-DD
    } catch (e) {
        return new Date().toISOString().split('T')[0];
    }
}

async function syncToNotion() {
    console.log('Reading jobs from local file...');
    const jobs = parseJobsFile(jobsFilePath);
    console.log(`Found ${jobs.length} jobs in jobs.md`);

    console.log('Validating Notion connection...');
    try {
        const response = await notion.users.me({});
        console.log('Authenticated as:', response.name || 'Antigravity Integration');
    } catch (error) {
        console.error('Authentication failed:', error.message);
        return;
    }

    // Attempt to access the database directly
    try {
        await notion.databases.retrieve({ database_id: databaseId });
        console.log('Database access verified.');
    } catch (error) {
        console.error('----------------------------------------------------');
        console.error('ERROR: Could not access the Notion Database.');
        console.error(`ID: ${databaseId}`);
        console.error('Reason:', error.message);
        console.error('Possible fixes:');
        console.error('1. Have you SHARED the database with the integration?');
        console.error('   (Click "..." on the database page -> "Add connections" -> Select your integration)');
        console.error('2. Is the Database ID correct?');
        console.error('----------------------------------------------------');
        return;
    }

    for (const job of jobs) {

        try {
            console.log(`Syncing NEW: ${job.title} at ${job.company}`);

            // Prepare properties
            const properties = {
                'Title': {
                    title: [{ text: { content: job.title } }]
                },

                'Company': {
                    rich_text: [{ text: { content: (job.company && job.company.length > 0) ? job.company : 'N/A' } }]
                },
                'Location': {
                    rich_text: [{ text: { content: job.location } }]
                },
                'Link': {
                    url: job.link
                },
                'DateScanned': {
                    date: { start: formatDate(job.date) }
                }
            };

            // Optional fields
            if (job.type) {
                properties['Type'] = {
                    select: { name: job.type.substring(0, 100) }
                };
            }
            if (job.stack) {
                const stackItems = job.stack.split(',')
                    .map(s => s.trim())
                    .filter(s => s.length > 0)
                    .map(s => ({ name: s.replace(/,/g, '').substring(0, 100) }));

                if (stackItems.length > 0) {
                    properties['TechStack'] = {
                        multi_select: stackItems
                    };
                }
            }
            if (job.summary) {
                properties['Summary'] = {
                    rich_text: [{ text: { content: job.summary.substring(0, 2000) } }]
                };
            }

            await notion.pages.create({
                parent: { database_id: databaseId },
                properties: properties
            });

        } catch (error) {
            console.error(`Failed to sync job ${job.title}:`, error.body || error.message);
        }
    }
    console.log('Sync complete!');
}

syncToNotion();
