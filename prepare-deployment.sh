#!/bin/bash
# Quick deployment script for HidenCloud

# Stop on error
set -e

echo "🚀 Preparing Background Removal Service for deployment..."

# 1. Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 2. Download the u2net model (so it's included in the deployment)
echo "🧠 Pre-downloading u2net model..."
python -c "from rembg import new_session; new_session('u2net')"

# 3. Run tests
echo "✅ Running basic test..."
python -m py_compile app.py

echo ""
echo "✨ Service is ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Update AUTH_TOKEN in .env to a secure value"
echo "2. Push to GitHub:"
echo "   git add . && git commit -m 'Ready for deployment' && git push"
echo "3. Go to https://dash.hidencloud.com/dashboard"
echo "4. Create new service and select Docker deployment"
echo "5. Connect your GitHub repository"
echo ""
