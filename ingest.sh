# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
# Error if any command fails
set -e
if [ $# -eq 0 ] then
    echo "Usage: ingest.py github-username"
    exit 1
fi
python3 ingest.py $1
