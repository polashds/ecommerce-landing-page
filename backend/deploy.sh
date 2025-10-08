#!/bin/bash

echo "🚀 Starting deployment process..."

# Check if all tests pass
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Aborting deployment."
    exit 1
fi

echo "✅ All tests passed!"

# Deploy to Heroku
git add .
git commit -m "Production deployment $(date '+%Y-%m-%d %H:%M:%S')"
git push heroku main

echo "🎉 Deployment completed!"