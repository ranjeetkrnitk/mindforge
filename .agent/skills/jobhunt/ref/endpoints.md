# Job Board Endpoints

## Greenhouse
Base URL: `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs`

| Company | Slug |
|---|---|
| Anthropic | anthropic |
| Stripe | stripe |
| OpenAI | openai |
| Figma | figma |
| Discord | discord |
| Notion | notion |
| Airtable | airtable |
| Airbnb | airbnb |
| DoorDash | doordash |
| Shopify | shopify |
| Netflix | netflix |
| Uber | uber |
| Lyft | lyft |
| GitHub | github |
| HashiCorp | hashicorp |
| MongoDB | mongodb |
| Databricks | databricks |
| Snowflake | snowflake |
| Scale AI | scaleai |
| Perplexity | perplexityai |
| Confluent | confluent |
| Datadog | datadoghq |
| Cloudflare | cloudflare |
| Twilio | twilio |
| Plaid | plaid |

## Lever
Base URL: `https://api.lever.co/v0/postings/{slug}`

| Company | Slug |
|---|---|
| Vercel | vercel |
| Palantir | palantir |
| Carta | carta |
| Rippling | rippling |
| Brex | brex |

## Ashby
Base URL: `https://api.ashbyhq.com/posting-public/job-board/{slug}/published`

| Company | Slug |
|---|---|
| Cursor | cursor |
| Cohere | cohere |
| Linear | linear |
| Loom | loom |
| Retool | retool |

## Web Search Fallback
For companies not listed above:
Query: `"{role}" jobs {location} {company} site:linkedin.com OR site:greenhouse.io OR site:lever.co OR site:ashbyhq.com`
