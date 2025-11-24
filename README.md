# Dockerized Linkedin Job Scraper

A containerized Python-based web scraping tool that extracts job listings from LinkedIn and exports them to CSV files. The application runs in a Docker container using Selenium with Chrome in headless mode.


## Overview

This tool automates the collection of LinkedIn job postings and organizes them into structured CSV files. Built on the `selenium/standalone-chrome` Docker image, it provides a consistent environment across Windows, macOS, and Linux platforms.

## Features

- Fully containerized using official `selenium/standalone-chrome` image
- Pre-built Docker image available on Docker Hub: `kaushallb/linkedin-scraper:1.0`
- Cross-platform compatibility (Windows, macOS, Linux)
- Persistent data storage via volume mounting
- Timestamped CSV output files
- Headless browser operation



## Prerequisites

- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))


## Installation

### Using Pre-built Docker Image

```bash
docker pull kaushallb/linkedin-scraper:1.0
mkdir jobs
docker run -v ${PWD}/jobs:/app/jobs kaushallb/linkedin-scraper:1.0
```

### Linux / macOS
```bash
docker pull kaushallb/linkedin-scraper:1.0
mkdir jobs
docker run --rm -v "$(pwd)/jobs:/app/jobs" kaushallb/linkedin-scraper:1.0
```

### Windows PowerShell
```bash
docker pull kaushallb/linkedin-scraper:1.0
mkdir jobs
docker run --rm -v "${PWD}\jobs:/app/jobs" kaushallb/linkedin-scraper:1.0
```

### Building from Source

```bash
git clone https://github.com/KaushallB/Automated-LinkedIn-Job-Scraper.git
cd Automated-LinkedIn-Job-Scraper
docker build -t linkedin-scraper .
```
### Linux/macOS
```bash
docker run --rm -v "$(pwd)/jobs:/app/jobs" linkedin-scraper
```

### Windows PowerShell
```bash
docker run --rm -v "${PWD}\jobs:/app/jobs" linkedin-scraper
```

## Container Components

The Docker image is based on `selenium/standalone-chrome` and includes:
- Google Chrome 
- ChromeDriver 
- Python 3.10
- Selenium 4.31.0
- Required system dependencies


## Usage

### Running the Container

```bash
docker run -v ${PWD}/jobs:/app/jobs kaushallb/linkedin-scraper:1.0
```

### Execution Process

1. Container initializes Chrome browser in headless mode
2. Navigates to specified LinkedIn jobs search URL
3. Dismisses sign-in popup automatically
4. Scrolls through job listings and extracts data
5. Saves results to timestamped CSV in `/app/jobs` directory
6. Displays progress messages and exits

### Customizing Search Parameters

You can use Your Own LinkedIn Search URL: 
1. Open your web browser and go to [LinkedIn Jobs](https://www.linkedin.com/jobs/) 
2. Enter your desired job title in the search box (e.g., "Software Engineer", "Data Analyst") 
3. Enter your preferred location (e.g., "Kathmandu", "New York", "Australia", ..) 
4. Apply any filters you want (date posted, experience level, job type, etc.) 
5. Copy the entire URL from your browser's address bar 
6. Open scraper.py and replace the URL on line 34 with your copied URL


## Output 

### File Location and Format 
CSV files are automatically saved in the jobs/ directory with the following naming convention:
jobs/job_listing_2025-11-18_14-30-25.csv
Format: job_listing_YYYY-MM-DD_HH-MM-SS.csv

### Accessing Results

View files on host machine:
```bash
ls jobs/
```

Access container filesystem:
```bash
docker exec -it <container-id> ls -la /app/jobs/
```

## Docker Commands

```bash
# Pull image
docker pull kaushallb/linkedin-scraper:1.0

# Run container
docker run -v ${PWD}/jobs:/app/jobs kaushallb/linkedin-scraper:1.0

# Build from source
docker build -t linkedin-scraper .

# View logs
docker logs <container-id>

# Access container
docker exec -it <container-id> bash

# View running containers
docker ps

# Stop and remove
docker stop <container-id>
docker rm <container-id>
```

## Volume Mounting

The `-v ${PWD}/jobs:/app/jobs` flag synchronizes data between:
- Host directory: `./jobs`
- Container directory: `/app/jobs`

Files created in the container's `/app/jobs` directory persist on the host machine after the container stops.

## Troubleshooting

### No CSV files created
Verify volume mount syntax:
```bash
# Windows PowerShell
docker run -v ${PWD}/jobs:/app/jobs kaushallb/linkedin-scraper:1.0

# Linux/Mac
docker run -v $(pwd)/jobs:/app/jobs kaushallb/linkedin-scraper:1.0
```

### Script stops after limited scrolling
- This is intentional behavior due to LinkedIn's automation detection 
- LinkedIn often stops loading new content when it detects automated browsing, causing the page to appear "stuck"
- The script uses max_scroll_attempts = 3 to automatically terminate when this occurs 
- Increase max_scroll_attempts if needed, but be aware this may not resolve LinkedIn's content loading restrictions 
- This limitation is a known issue with LinkedIn's anti-bot measures during automated scraping

## Disclaimer

This tool is intended for educational use only. Web scraping may violate LinkedIn's Terms of Service. Users are responsible for compliance with applicable terms and laws.


