#!/bin/bash
# DEPLOYMENT CHECKLIST SCRIPT
# This script verifies your carousel is ready for deployment

echo "🚀 Starting Deployment Verification..."
echo ""

# Check if files exist
echo "📁 Checking project files..."
if [ -f "index.html" ]; then echo "  ✅ index.html found"; else echo "  ❌ index.html missing"; fi
if [ -f "styles.css" ]; then echo "  ✅ styles.css found"; else echo "  ❌ styles.css missing"; fi
if [ -f "script.js" ]; then echo "  ✅ script.js found"; else echo "  ❌ script.js missing"; fi
echo ""

# Check HTML validity
echo "🔍 Checking HTML structure..."
if grep -q "<!DOCTYPE html>" index.html; then echo "  ✅ DOCTYPE found"; else echo "  ⚠️  DOCTYPE missing"; fi
if grep -q "<meta name=\"viewport\"" index.html; then echo "  ✅ Viewport meta tag found"; else echo "  ⚠️  Viewport meta tag missing"; fi
if grep -q "carousel" index.html; then echo "  ✅ Carousel markup found"; else echo "  ❌ Carousel markup missing"; fi
echo ""

# Check CSS
echo "📋 Checking CSS..."
if grep -q "perspective" styles.css; then echo "  ✅ 3D perspective found"; else echo "  ⚠️  3D perspective missing"; fi
if grep -q "@keyframes" styles.css; then echo "  ✅ Animations found"; else echo "  ❌ Animations missing"; fi
if grep -q "transition" styles.css; then echo "  ✅ Transitions found"; else echo "  ⚠️  Transitions missing"; fi
echo ""

# Check JavaScript
echo "🔧 Checking JavaScript..."
if grep -q "class Carousel" script.js; then echo "  ✅ Carousel class found"; else echo "  ❌ Carousel class missing"; fi
if grep -q "DOMContentLoaded" script.js; then echo "  ✅ Event listeners found"; else echo "  ⚠️  Event listeners missing"; fi
if grep -q "autoPlayInterval" script.js; then echo "  ✅ Auto-play logic found"; else echo "  ⚠️  Auto-play logic missing"; fi
echo ""

# File sizes
echo "📊 File sizes..."
echo "  index.html: $(wc -l < index.html) lines"
echo "  styles.css: $(wc -l < styles.css) lines"
echo "  script.js: $(wc -l < script.js) lines"
echo ""

echo "════════════════════════════════════════"
echo "✅ Pre-Deployment Verification Complete!"
echo "════════════════════════════════════════"
echo ""
echo "📝 Next steps:"
echo "  1. Review image URLs in index.html"
echo "  2. Test locally: python -m http.server 8000"
echo "  3. Check browser console for errors (F12)"
echo "  4. Test on mobile devices"
echo "  5. Deploy to hosting provider"
echo ""
echo "🎯 Ready to deploy? Run one of these commands:"
echo "  - Vercel: vercel"
echo "  - Netlify: netlify deploy --prod"
echo "  - GitHub Pages: git push origin main"
echo ""
