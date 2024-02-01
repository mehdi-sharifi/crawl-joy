# Bama Ads Crawler

## Overview
This Python project is designed to crawl Bama ads and extract relevant information for further analysis. It utilizes web scraping techniques to gather data from the Bama website.

## Features
- Web scraping Bama ads for extracting relevant data.
- Helm charts for easy deployment using Kubernetes.

## Prerequisites
- Python 3.8
- Helm 
- Kubernetes cluster (optional, for deployment)

## Setup
git clone git@github.com:mehdi-sharifi/crawl-joy.git
cd crawl-joy
to check the notification you can put yout email address in "/helm/crawler-app/valuses.yaml => 'sampleemailaddress' "

bash deploy-on-k8s.sh (or manually run the helms)

