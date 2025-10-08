#!/bin/bash

echo "🚀 Deploying frontend..."

# Build the project
npm run build

# Deploy to Vercel
vercel --prod

echo "🎉 Frontend deployed!"