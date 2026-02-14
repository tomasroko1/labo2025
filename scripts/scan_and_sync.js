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

// JSearch API Configuration
const RAPIDAPI_KEY = process.env.RAPIDAPI_KEY;
const RAPIDAPI_HOST = 'jsearch.p.rapidapi.com';

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

// Search jobs using JSearch API
async function searchJobs() {
    const options = {
        method: 'GET',
        url: 'https://jsearch.p.rapidapi.com/search',
        headers: {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': RAPIDAPI_HOST
        },
        params: {
            query: 'Data Engineer OR Data Scientist OR Python Developer',
            page: '1',
            num_pages: '1',
            date_posted: 'week'
        }
    };

    try {
        console.log('Searching jobs via JSearch API...');
        console.log('Query params:', options.params);
        const response = await axios.request(options);
        
        console.log('API Response status:', response.status);
        
        if (response.data && response.data.data) {
            console.log(`Found ${response.data.data.length} total jobs from API`);
            return response.data.data;
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
        const title = (job.job_title || '').toLowerCase();
        const description = (job.job_description || '').toLowerCase();
        const text = title + ' ' + description;
        
        // Exclude senior roles
        const hasExcludeKeyword = excludeKeywords.some(kw => text.includes(kw));
        if (hasExcludeKeyword) return false;
        
        // Must include at least one relevant keyword
        const hasIncludeKeyword = includeKeywords.some(kw => text.includes(kw));
        if (!hasIncludeKeyword) return false;
        
        // Check if it's part-time or internship
        const isPartTime = 
            text.includes('part-time') || 
            text.includes('part time') || 
            text.includes('media jornada') ||
            text.includes('pasantía') ||
            text.includes('pasante') ||
            text.includes('becario') ||
            text.includes('beca') ||
            text.includes('intern') ||
            text.includes('internship') ||
            text.includes('trainee') ||
            text.includes('estudiante') ||
            text.includes('20 horas') ||
            text.includes('20hrs') ||
            text.includes('flexible') ||
            job.job_employment_type === 'PARTTIME' ||
            job.job_employment_type === 'INTERN';
        
        return isPartTime;
    });
    
    console.log(`${filtered.length} jobs match part-time/internship criteria`);
    return filtered;
}

// Helper: Sync to Notion
async function syncJobToNotion(job) {
    try {
        // Extract tech stack keywords from description
        const techKeywords = ['python', 'sql', 'aws', 'azure', 'gcp', 'spark', 'hadoop', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'airflow', 'dbt', 'tableau', 'power bi', 'excel', 'javascript', 'typescript', 'react', 'node.js', 'git', 'github', 'ci/cd', 'terraform', 'etl', 'ml', 'machine learning', 'ai', 'statistics', 'r', 'jupyter'];
        
        const description = (job.job_description || '').toLowerCase();
        const stack = techKeywords
            .filter(kw => description.includes(kw))
            .map(kw => kw.charAt(0).toUpperCase() + kw.slice(1));
        
        // Determine job type
        let jobType = job.job_employment_type || 'Unknown';
        if (jobType === 'PARTTIME') jobType = 'Part-time';
        else if (jobType === 'INTERN') jobType = 'Internship';
        else if (jobType === 'CONTRACTOR') jobType = 'Contract';
        else if (jobType === 'FULLTIME') jobType = 'Full-time';
        
        // Truncate summary to 2000 chars (Notion limit)
        const summary = (job.job_description || 'No description available').substring(0, 2000);
        
        await notion.pages.create({
            parent: { database_id: databaseId },
            properties: {
                'Title': { 
                    title: [{ text: { content: job.job_title || 'Unknown Title' } }] 
                },
                'Company': { 
                    rich_text: [{ text: { content: job.employer_name || 'Unknown Company' } }] 
                },
                'Location': { 
                    rich_text: [{ 
                        text: { content: `${job.job_city || ''}, ${job.job_country || ''}`.trim() || 'Remote/Unknown' } 
                    }] 
                },
                'Link': { 
                    url: job.job_apply_link || job.job_google_link || job.job_highlights?.Apply || 'https://www.google.com' 
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
        console.log(`✅ Synced to Notion: ${job.job_title} at ${job.employer_name}`);
    } catch (error) {
        console.error(`❌ Failed to sync to Notion: ${error.message}`);
    }
}

// Main function
(async () => {
    try {
        console.log('=== LinkedIn Job Scraper via JSearch API ===');
        console.log('');
        
        // Get existing jobs
        const existingLinks = await getExistingJobLinksFromNotion();
        
        // Search for new jobs
        const allJobs = await searchJobs();
        
        if (allJobs.length === 0) {
            console.log('No jobs found from API');
            return;
        }
        
        // Filter for part-time/internship
        const filteredJobs = filterJobs(allJobs);
        
        if (filteredJobs.length === 0) {
            console.log('No part-time/internship jobs found matching criteria');
            return;
        }
        
        // Filter out existing jobs
        const newJobs = filteredJobs.filter(job => {
            const link = job.job_apply_link || job.job_google_link || job.job_highlights?.Apply;
            return link && !existingLinks.has(link);
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
            console.log(`Processing: ${job.job_title} at ${job.employer_name}`);
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
