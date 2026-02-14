const axios = require('axios');
const { Client } = require('@notionhq/client');

// Log environment variables for debugging
console.log('Environment check:');
console.log('NOTION_TOKEN exists:', !!process.env.NOTION_TOKEN);
console.log('NOTION_DATABASE_ID exists:', !!process.env.NOTION_DATABASE_ID);
console.log('RAPIDAPI_KEY exists:', !!process.env.RAPIDAPI_KEY);

if (!process.env.NOTION_TOKEN) {
    console.error('ERROR: NOTION_TOKEN is not set!');
    process.exit(1);
}

if (!process.env.NOTION_DATABASE_ID) {
    console.error('ERROR: NOTION_DATABASE_ID is not set!');
    process.exit(1);
}

if (!process.env.RAPIDAPI_KEY) {
    console.error('ERROR: RAPIDAPI_KEY is not set!');
    process.exit(1);
}

const notion = new Client({ auth: process.env.NOTION_TOKEN });
const databaseId = process.env.NOTION_DATABASE_ID;

// LinkedIn Job Search API Configuration
const RAPIDAPI_KEY = process.env.RAPIDAPI_KEY;
const RAPIDAPI_HOST = 'linkedin-job-search-api.p.rapidapi.com';

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
                    links.add(page.properties.Link.url);
                }
            }

            if (!response.has_more) {
                break;
            }
            cursor = response.next_cursor;
        }
    } catch (error) {
        console.error('Error querying Notion database:', error.message);
        throw error;
    }
    
    console.log(`Found ${links.size} existing jobs in Notion`);
    return links;
}

// Search jobs using LinkedIn Job Search API
async function searchJobs() {
    const options = {
        method: 'GET',
        url: 'https://linkedin-job-search-api.p.rapidapi.com/jobs',
        headers: {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': RAPIDAPI_HOST
        },
        params: {
            title_filter: '("Data Engineer" OR "Data Scientist" OR "Python Developer")',
            location_filter: 'Argentina',
            type_filter: 'PART_TIME,INTERN',
            limit: '20',
            description_type: 'text'
        }
    };

    try {
        console.log('Searching jobs via LinkedIn Job Search API...');
        console.log('Query:', options.params.title_filter);
        console.log('Location:', options.params.location_filter);
        console.log('Type:', options.params.type_filter);
        
        const response = await axios.request(options);
        
        console.log('API Response status:', response.status);
        
        if (response.data && Array.isArray(response.data)) {
            console.log(`Found ${response.data.length} total jobs from LinkedIn API`);
            return response.data;
        }
        return [];
    } catch (error) {
        console.error('Error searching jobs:', error.response?.data || error.message);
        return [];
    }
}

// Filter jobs based on criteria
function filterJobs(jobs) {
    const excludeKeywords = ['senior', 'lead', 'manager', 'architect', 'director', 'principal', 'head of'];
    const includeKeywords = ['data', 'engineer', 'scientist', 'python', 'sql', 'analyst', 'junior', 'intern', 'trainee', 'student', 'becario', 'pasantía', 'part-time', 'part time'];
    
    const filtered = jobs.filter(job => {
        const title = (job.title || '').toLowerCase();
        const description = (job.description_text || '').toLowerCase();
        const text = title + ' ' + description;
        
        // Exclude senior roles
        const hasExcludeKeyword = excludeKeywords.some(kw => text.includes(kw));
        if (hasExcludeKeyword) return false;
        
        // Must include at least one relevant keyword
        const hasIncludeKeyword = includeKeywords.some(kw => text.includes(kw));
        if (!hasIncludeKeyword) return false;
        
        return true;
    });
    
    console.log(`${filtered.length} jobs match criteria after filtering`);
    return filtered;
}

// Helper: Sync to Notion
async function syncJobToNotion(job) {
    try {
        // Extract tech stack keywords from description
        const techKeywords = ['python', 'sql', 'aws', 'azure', 'gcp', 'spark', 'hadoop', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'airflow', 'dbt', 'tableau', 'power bi', 'excel', 'javascript', 'typescript', 'react', 'node.js', 'git', 'github', 'ci/cd', 'terraform', 'etl', 'ml', 'machine learning', 'ai', 'statistics', 'r', 'jupyter'];
        
        const description = (job.description_text || '').toLowerCase();
        const stack = techKeywords
            .filter(kw => description.includes(kw))
            .map(kw => kw.charAt(0).toUpperCase() + kw.slice(1));
        
        // Determine job type from employment_type array
        let jobType = 'Unknown';
        if (job.employment_type && job.employment_type.length > 0) {
            const type = job.employment_type[0];
            if (type === 'PART_TIME') jobType = 'Part-time';
            else if (type === 'INTERN') jobType = 'Internship';
            else if (type === 'FULL_TIME') jobType = 'Full-time';
            else if (type === 'CONTRACTOR') jobType = 'Contract';
            else jobType = type;
        }
        
        // Get location from locations_derived array
        let location = 'Remote/Unknown';
        if (job.locations_derived && job.locations_derived.length > 0) {
            const loc = job.locations_derived[0];
            location = `${loc.city || ''}, ${loc.country || ''}`.trim() || 'Remote/Unknown';
        }
        
        // Truncate summary to 2000 chars (Notion limit)
        const summary = (job.description_text || 'No description available').substring(0, 2000);
        
        await notion.pages.create({
            parent: { database_id: databaseId },
            properties: {
                'Title': { 
                    title: [{ text: { content: job.title || 'Unknown Title' } }] 
                },
                'Company': { 
                    rich_text: [{ text: { content: job.organization || 'Unknown Company' } }] 
                },
                'Location': { 
                    rich_text: [{ text: { content: location } }] 
                },
                'Link': { 
                    url: job.url || 'https://www.linkedin.com' 
                },
                'DateScanned': { 
                    date: { start: new Date().toISOString().split('T')[0] } 
                },
                'Type': { 
                    select: { name: jobType.substring(0, 100) } 
                },
                'TechStack': {
                    multi_select: stack.slice(0, 20).map(s => ({ name: s.substring(0, 100) }))
                },
                'Summary': { 
                    rich_text: [{ text: { content: summary } }] 
                }
            }
        });
        console.log(`✅ Synced to Notion: ${job.title} at ${job.organization}`);
    } catch (error) {
        console.error(`❌ Failed to sync to Notion: ${error.message}`);
    }
}

// Main function
(async () => {
    try {
        console.log('=== LinkedIn Job Scraper (Real LinkedIn API) ===');
        console.log('');
        
        // Get existing jobs
        const existingLinks = await getExistingJobLinksFromNotion();
        
        // Search for new jobs
        const allJobs = await searchJobs();
        
        if (allJobs.length === 0) {
            console.log('No jobs found from LinkedIn API');
            return;
        }
        
        // Filter jobs
        const filteredJobs = filterJobs(allJobs);
        
        if (filteredJobs.length === 0) {
            console.log('No jobs found matching criteria');
            return;
        }
        
        // Filter out existing jobs
        const newJobs = filteredJobs.filter(job => {
            return job.url && !existingLinks.has(job.url);
        });
        
        console.log(`${newJobs.length} new jobs to process`);
        
        if (newJobs.length === 0) {
            console.log('No new jobs to sync');
            return;
        }
        
        // Process only first 7 jobs
        const jobsToProcess = newJobs.slice(0, 7);
        console.log(`Processing ${jobsToProcess.length} jobs...`);
        console.log('');
        
        for (const job of jobsToProcess) {
            console.log(`Processing: ${job.title} at ${job.organization}`);
            await syncJobToNotion(job);
            
            // Small delay to be polite
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        console.log('');
        console.log('=== Job sync complete ===');
        
    } catch (error) {
        console.error('Fatal error:', error);
        process.exit(1);
    }
})();
