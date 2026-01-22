# Frontend Deployment Guide

## Environment Variables

The frontend requires one environment variable to connect to the backend:

```
VITE_API_BASE_URL=https://dataset-management-platform-production.up.railway.app
```

### Local Development
- Uses `.env` file (already configured for localhost:8000)
- Automatically falls back to localhost if VITE_API_BASE_URL is not set

### Netlify Deployment

1. **Build Settings**
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Base directory: `frontend`

2. **Environment Variables**
   - Go to Site Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://dataset-management-platform-production.up.railway.app`

3. **Redirects**
   - The `public/_redirects` file is already configured
   - Ensures React Router works on page refresh
   - All routes redirect to index.html (SPA behavior)

## Files Modified

### 1. `src/services/api.js`
- **Changed:** Uses `import.meta.env.VITE_API_BASE_URL` with localhost fallback
- **Purpose:** Connect to Railway backend in production, localhost in dev

### 2. `public/_redirects` (NEW)
- **Purpose:** Netlify SPA routing - prevents 404 on direct route access

### 3. `.env` (NEW)
- **Purpose:** Local development environment variables (localhost)

### 4. `.env.example` (NEW)
- **Purpose:** Documents required environment variables for deployment

### 5. `.gitignore` (NEW)
- **Purpose:** Prevents .env files from being committed

## Testing Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on http://localhost:3000 and connect to http://localhost:8000

## Deployment Checklist

- [ ] Backend deployed on Railway
- [ ] Frontend repo connected to Netlify
- [ ] Environment variable `VITE_API_BASE_URL` set on Netlify
- [ ] Build settings configured (build command, publish directory)
- [ ] First deployment successful
- [ ] Test login/logout flow
- [ ] Test direct navigation to /datasets
- [ ] Test page refresh on protected routes
