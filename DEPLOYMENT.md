# 🚀 Deployment Guide - 3D Animated Carousel

## Quick Deployment Options

### Option 1: Deploy to Vercel (Recommended - 30 seconds)
```bash
1. Install Vercel CLI: npm i -g vercel
2. Navigate to your project: cd path/to/focusmirror
3. Deploy: vercel
4. Follow prompts, done! Your site is live.
```
**Link**: `https://your-project.vercel.app`

---

### Option 2: Deploy to Netlify (30 seconds)
```bash
1. Drag & drop the folder to https://app.netlify.com
   OR
2. Install Netlify CLI: npm i -g netlify-cli
3. Run: netlify deploy --prod --dir=.
```
**Link**: `https://your-project.netlify.app`

---

### Option 3: Deploy to GitHub Pages (Free)
```bash
1. Create a GitHub repository
2. Push your files: git push origin main
3. Go to Settings → Pages → Select "main" branch
4. Your site is live at: https://yourusername.github.io/focusmirror
```

---

### Option 4: Self-Hosted (Your own server)
```bash
1. Upload all files to your web server via FTP/SFTP
2. Ensure index.html is in the root directory
3. Access via your domain: https://yourdomain.com
```

---

### Option 5: Local Testing with Live Server
```bash
# Using Python (built-in on most systems)
cd path/to/focusmirror
python -m http.server 8000

# OR using Node.js
npx http-server

# Then visit: http://localhost:8000
```

---

## Pre-Deployment Checklist

- [ ] All image URLs are working and accessible
- [ ] Button links are configured (`cta-button` href)
- [ ] Title, subtitle, and stats are customized
- [ ] Background gradient matches your brand
- [ ] Tested on mobile devices (iPhone, Android)
- [ ] Tested on browsers (Chrome, Firefox, Safari, Edge)
- [ ] Images are compressed and optimized
- [ ] No console errors (`F12` → Console tab)
- [ ] All links work properly
- [ ] Meta tags updated in `index.html` (title, description)

---

## Post-Deployment Checklist

- [ ] Site loads without 404 errors
- [ ] 3D carousel animations work smoothly
- [ ] Navigation buttons respond correctly
- [ ] Images load properly
- [ ] Touch/swipe works on mobile
- [ ] Parallax effect works on desktop
- [ ] Performance is acceptable (test with Lighthouse)
- [ ] SEO meta tags are present
- [ ] Mobile-friendly viewport looks good

---

## Optimization Tips Before Deployment

### 1. Optimize Images
```bash
# Using ImageOptim (Mac) or similar tools:
# Compress all images to reduce file size
# Target: < 100KB per image
```

### 2. Minify Code (Optional)
```bash
# CSS minification
# JS minification
# Use online tools or build scripts
```

### 3. Enable GZIP Compression
Most hosting providers do this automatically. Verify in your server settings.

### 4. Add a Service Worker for Offline Support
See `service-worker.js` example below.

### 5. Performance Testing
- Google PageSpeed: https://pagespeed.web.dev
- GTmetrix: https://gtmetrix.com
- WebPageTest: https://www.webpagetest.org

---

## Deployment Status Messages

### When deploying, you'll see:
```
✅ Building...
✅ Uploading files...
✅ Configuring server...
✅ Domain setup...
✅ Deployment complete!
🎉 Your site is live at: [URL]
```

---

## Common Issues & Fixes

### Issue: Images show broken (404 error)
**Fix**: 
- Use absolute URLs or correct relative paths
- Verify image host accessibility
- Add CORS headers if needed

### Issue: Animations are choppy/laggy
**Fix**:
- Reduce number of carousel items
- Optimize image file sizes
- Enable hardware acceleration

### Issue: Site doesn't load (white screen)
**Fix**:
- Check browser console for errors (`F12`)
- Verify all file paths are correct
- Ensure `index.html` is in root directory

### Issue: Mobile doesn't work
**Fix**:
- Check viewport meta tag in HTML
- Test touch events
- Verify CSS media queries

---

## Environment Setup by Platform

### Vercel Environment Variables (optional)
```bash
# .env.local file
NEXT_PUBLIC_CAROUSEL_ITEMS=5
NEXT_PUBLIC_AUTO_PLAY_INTERVAL=5000
```

### Netlify Environment Variables
Build settings → Environment → Add variables

### GitHub Pages (No additional setup needed)

---

## Monitoring & Analytics

### Add Google Analytics
```html
<!-- Add to <head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Monitor uptime
- UptimeRobot: https://uptimerobot.com (free)
- StatusPage: https://www.statuspage.io

---

## Support & Troubleshooting

**Need help?**
- Check console errors: Press `F12` → Console
- Test locally first: Use Live Server
- Verify all file paths
- Check image URLs are accessible

**Still having issues?**
- Review the README.md
- Check CUSTOMIZATION.md for common changes
- Verify CORS policies for external resources

---

## Next Steps After Deployment

1. **Share your carousel**: Copy the live URL
2. **Track analytics**: Monitor traffic and user behavior
3. **Get feedback**: Test with real users
4. **Iterate**: Update images/content as needed
5. **Promote**: Share on social media

---

**Your carousel is ready to go live! 🚀**
