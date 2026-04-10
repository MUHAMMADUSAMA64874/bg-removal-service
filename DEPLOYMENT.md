# HidenCloud Deployment Guide

## Prerequisites

1. HidenCloud account with dashboard access: https://dash.hidencloud.com/dashboard
2. Recommended: Docker installed locally for testing

## Deployment Option 1: Using Docker (Recommended)

### Step 1: Build Docker Image Locally (Optional Test)

```bash
cd bg-removal-service
docker build -t bg-removal-service:latest .
docker run -p 8000:8000 -e AUTH_TOKEN="your-secure-token" bg-removal-service:latest
```

Test at http://localhost:8000/

### Step 2: Deploy to HidenCloud

1. Log in to https://dash.hidencloud.com/dashboard
2. Click **Create** or **New Service**
3. Select **Docker** or **Container** deployment
4. Choose deployment method:
   - **Option A**: Upload Dockerfile directly
   - **Option B**: Push to Docker registry and reference the image
   - **Option C**: Connect GitHub repo with Dockerfile

5. Configure environment variables in HidenCloud dashboard:
   - `AUTH_TOKEN`: Set your secure token
   - `PORT`: Keep as 8000 (or adjust if needed)

6. Set port: `8000` (expose to internet)
7. Click **Deploy**

## Deployment Option 2: Direct Python (If HidenCloud Supports)

### Without Docker

1. Upload all files to HidenCloud:
   - app.py
   - requirements.txt
   - static/ (folder)
   - .env

2. Set start command:
   ```
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. Set Python version: 3.11 or higher

## Deployment Option 3: GitHub Integration

1. Push your code to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/bg-removal-service
   git push -u origin main
   ```

2. In HidenCloud dashboard:
   - Select **GitHub** as source
   - Connect your GitHub account
   - Select your repository
   - HidenCloud will auto-detect the Dockerfile and deploy

## After Deployment

### Update Your React App

Replace the endpoint in your React application:

```javascript
// Old: remove.bg API
const REMOVE_BG_URL = "https://api.remove.bg/v1/removebg";

// New: Your deployed service
const REMOVE_BG_URL = "https://your-hidencloud-domain.com";

const removeBackground = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('token', 'your-secure-token');

  const response = await fetch(`${REMOVE_BG_URL}/remove-bg`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Background removal failed');
  }

  return await response.blob();
};
```

### Security Notes

1. Change `AUTH_TOKEN` to a strong random value before deployment
2. Set HTTPS (HidenCloud usually handles this automatically)
3. Store `AUTH_TOKEN` securely - don't commit it in code
4. Consider adding rate limiting or request signing for production

## Domain Setup (HidenCloud)

After deployment:
1. Go to **Settings** → **Domain**
2. Configure custom domain or use HidenCloud's subdomain
3. Copy the URL to your React app

## Monitoring & Logs

In HidenCloud dashboard:
- View logs in **Logs** section
- Monitor resource usage in **Metrics**
- Set up alerts if available

## Troubleshooting

### Model Download Issues
If deployment fails during model download:
- Build Docker image with pre-downloaded models
- Or increase timeout in HidenCloud settings

### File Size Issues
- Current limit: 10MB (configurable in app.py)
- Edit `MAX_FILE_SIZE` if needed

### Performance
- If slow, change model to `u2netp` (faster, lower quality)
- Edit line with `new_session("u2net")` to `new_session("u2netp")`

## Support

- HidenCloud Docs: https://docs.hidencloud.com (if available)
- FastAPI Docs: https://fastapi.tiangolo.com
- rembg GitHub: https://github.com/danielgatis/rembg
