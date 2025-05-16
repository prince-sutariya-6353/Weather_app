# Deploying Your Weather App to Vercel

This guide will help you deploy your Flask Weather App to Vercel, making it accessible online.

## Prerequisites

1. A [GitHub](https://github.com/) account
2. A [Vercel](https://vercel.com/) account (you can sign up using your GitHub account)
3. [Git](https://git-scm.com/) installed on your computer

## Step 1: Prepare Your Repository

1. Make sure your project has all the necessary files:

   - `app.py` - Main Flask application
   - `templates/index.html` - HTML template
   - `requirements.txt` - All project dependencies
   - `vercel.json` - Vercel configuration file
   - `api/index.py` - Serverless function entry point

2. Initialize a Git repository (if you haven't already):

   ```
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```

3. Create a repository on GitHub and push your code:
   ```
   git remote add origin https://github.com/YOUR_USERNAME/weather-app.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Set Up Environment Variables on Vercel

Before deploying, you'll need to set up your environment variables:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Create a new project or select your existing project
3. Go to the "Settings" tab
4. Select "Environment Variables"
5. Add the following variables:
   - `WEATHER_API_KEY` - Your OpenWeatherMap API key
   - `SECRET_KEY` - A secure random string for Flask sessions

## Step 3: Deploy to Vercel

1. Install Vercel CLI (optional):

   ```
   npm i -g vercel
   ```

2. Deploy using Vercel CLI (optional):

   ```
   vercel
   ```

3. Alternative: Deploy directly from GitHub:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Configure your project settings (ensure Python is selected as the framework)
   - Click "Deploy"

## Step 4: Test Your Deployment

After deployment, Vercel will provide you with a URL for your application. Visit the URL to ensure your Weather App is working correctly.

## Troubleshooting

If you encounter any issues:

1. Check the Vercel logs in your project dashboard
2. Ensure all environment variables are set correctly
3. Verify that your requirements.txt has all necessary dependencies
4. Make sure the vercel.json configuration is correct

## Making Updates

To update your application:

1. Make changes to your local repository
2. Commit and push to GitHub:

   ```
   git add .
   git commit -m "Description of changes"
   git push
   ```

3. Vercel will automatically deploy the updated version (if you've set up automatic deployments)

## Notes on Sessions

For production use, you may want to consider using a server-side session store instead of Flask's default client-side sessions. This becomes important when using stateless serverless functions.
