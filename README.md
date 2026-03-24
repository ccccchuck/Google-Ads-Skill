# Google Ads Skill for Open Claw

A comprehensive Google Ads data fetching and analysis skill for the Open Claw agentic platform.

## Features
- **Authentication**: Auto-generates OAuth2 refresh tokens for API access.
- **Reporting**: Fetches keyword performance, campaign metrics, and search term reports.
- **Analysis**: Intelligent insights and ad-spend optimization recommendations based on actual performance data.

## Setup
1. Ensure you have a Google Ads Developer Token.
2. Provide your OAuth2 `client_secret.json` credentials.
3. Configure `google-ads.yaml` and authenticate using the `ads-setup` sub-skill.

## Structure
- `SKILL.md`: Main entry point and intent routing.
- `skills/`: Sub-skills for specific operations (setup, fetch, analyze, report).
- `scripts/`: Python scripts to interact with the Google Ads API.
