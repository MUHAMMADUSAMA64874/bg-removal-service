# Background Removal Service

A FastAPI service for removing image backgrounds using rembg.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate and install dependencies:
   ```bash
   # Windows
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running Locally

```bash
# Activate venv first
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at http://localhost:8000

## GUI Test Page

Open this URL in your browser after starting the server:

- http://localhost:8000/

This page lets you upload an image, provide the auth token, and view the result directly.

## API

### POST /remove-bg

Remove background from uploaded image.

**Headers:**
- Authorization: Bearer your-secret-token

**Body:** Multipart form data
- file: Image file (JPEG, PNG, WebP, BMP, TIFF)
- token: your-secret-token (alternative to header)

**Response:** PNG image with background removed

**Limits:**
- Max file size: 10MB
- Allowed types: image/jpeg, image/png, image/webp, image/bmp, image/tiff

## Testing

Use Postman or curl:

```bash
curl -X POST "http://localhost:8000/remove-bg" \
  -H "Authorization: Bearer your-secret-token" \
  -F "file=@image.jpg"
```

## Deployment to HidenCloud

### Prerequisites
- GitHub account with git repository
- HidenCloud account at https://dash.hidencloud.com/dashboard

### Step 1: Prepare for Deployment

1. Update your auth token in `.env`:
   ```
   AUTH_TOKEN=your-very-secure-random-token-here
   ```

2. Initialize Git and push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Background removal service ready for deployment"
   git remote add origin https://github.com/YOUR-USERNAME/bg-removal-service
   git push -u origin main
   ```

### Step 2: Deploy via HidenCloud

1. Go to https://dash.hidencloud.com/dashboard
2. Click **Create New Service** or **Deploy**
3. Select **Docker** deployment method
4. Choose **GitHub** as source
5. Connect your GitHub account and select your repository
6. HidenCloud will auto-detect the Dockerfile

### Step 3: Configure Environment

In HidenCloud dashboard:
- Add environment variable: `AUTH_TOKEN=your-very-secure-token`
- Set port: `8000`
- Enable HTTPS/SSL

### Step 4: Get Your URL

After deployment completes:
- Copy your deployment URL from HidenCloud dashboard
- Format: `https://your-service-name.hidencloud.com` (or similar)

### Step 5: Update React App

Update your remove.bg API calls:

```javascript
const DEPLOYED_URL = "https://your-service-name.hidencloud.com";

const removeBackground = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('token', 'your-very-secure-token'); // Store in env var in React

  const response = await fetch(`${DEPLOYED_URL}/remove-bg`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Background removal failed');
  }

  return await response.blob();
};
```

### More Details

See [DEPLOYMENT.md](DEPLOYMENT.md) for advanced options and troubleshooting.

## React Integration

Replace your remove.bg API call with:

```javascript
const removeBackground = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('token', 'your-secret-token');

  const response = await fetch('https://your-deployed-service.com/remove-bg', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Background removal failed');
  }

  return await response.blob();
};
```

Then use the returned blob as before in your layer/update flow.