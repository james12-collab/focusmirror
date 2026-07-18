<!-- QUICK CUSTOMIZATION GUIDE -->

<!-- 
This file shows you exactly what to change to customize the carousel quickly.
Copy-paste from examples below into your index.html
-->

<!-- ============================================ -->
<!-- 1. CHANGE IMAGES -->
<!-- ============================================ -->

<!-- Original: -->
<img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=600&fit=crop" alt="Mountain View">

<!-- Your custom image: -->
<img src="https://YOUR_DOMAIN.com/images/your-image.jpg" alt="Your Description">

<!-- Pro Tips:
   - Use 600x600px images for best results
   - Compress images to reduce load time
   - Use CORS-friendly image hosts
   - Alt text helps with SEO -->


<!-- ============================================ -->
<!-- 2. CHANGE GRADIENT COLORS -->
<!-- ============================================ -->

<!-- 
Find this in index.html and modify the gradient:

Original:
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">

Change to any of these:
-->

<!-- Purple to Pink -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">

<!-- Coral to Orange -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">

<!-- Blue to Cyan -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">

<!-- Red to Yellow -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">

<!-- Dark Blue to Purple -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">

<!-- Green to Teal -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">

<!-- Orange to Red -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);">

<!-- Pro Tips:
   - Use websites like coolors.co or gradientos.app
   - Keep gradients at 135deg or 45deg for consistency
   - Test colors against your images for contrast -->


<!-- ============================================ -->
<!-- 3. CHANGE TITLE AND DESCRIPTION -->
<!-- ============================================ -->

<!-- Find in index.html and modify: -->

<!-- Original: -->
<h1 class="title">Similar</h1>
<p class="subtitle">Discover amazing moments</p>

<!-- Change to: -->
<h1 class="title">Your Title Here</h1>
<p class="subtitle">Your description here</p>


<!-- ============================================ -->
<!-- 4. CHANGE BUTTON TEXT -->
<!-- ============================================ -->

<!-- Original: -->
<button class="cta-button">Explore Now</button>

<!-- Change to: -->
<button class="cta-button">Shop Now</button>
<button class="cta-button">View Gallery</button>
<button class="cta-button">Get Started</button>
<button class="cta-button">Learn More</button>


<!-- ============================================ -->
<!-- 5. CHANGE STATISTICS -->
<!-- ============================================ -->

<!-- Original: -->
<div class="stat">
    <span class="label">Rating</span>
    <span class="value">5.0</span>
</div>
<div class="stat">
    <span class="label">Completed</span>
    <span class="value">1 project</span>
</div>

<!-- Change to: -->
<div class="stat">
    <span class="label">Downloads</span>
    <span class="value">1M+</span>
</div>
<div class="stat">
    <span class="label">Users</span>
    <span class="value">500K+</span>
</div>


<!-- ============================================ -->
<!-- 6. ADD MORE CAROUSEL ITEMS -->
<!-- ============================================ -->

<!-- 
Add as many as you want! Just copy this structure:
(Don't forget to add a corresponding dot button too!)
-->

<!-- New carousel item: -->
<div class="carousel-item" style="--bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="item-inner">
        <div class="image-frame">
            <img src="https://images.unsplash.com/photo-YOUR-IMAGE?w=600&h=600&fit=crop" alt="Your Image">
        </div>
    </div>
</div>

<!-- Add corresponding dot button: -->
<button class="dot" data-index="5"></button>


<!-- ============================================ -->
<!-- 7. ADJUST ANIMATION SPEED (JAVASCRIPT) -->
<!-- ============================================ -->

/* In script.js, find this line (around line 68): */
this.autoPlayInterval = setInterval(() => {
    this.next();
}, 5000);  /* <-- Change 5000 to your desired milliseconds */

/* Examples:
   3000 = 3 seconds (fast)
   5000 = 5 seconds (normal)
   8000 = 8 seconds (slow)
   10000 = 10 seconds (very slow)
*/


<!-- ============================================ -->
<!-- 8. ADJUST ANIMATION TIMING (CSS) -->
<!-- ============================================ -->

/* In styles.css, find these transitions: */

.carousel-item {
    transition: all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    /*                  ^^^ Change this value */
}

/* Timing presets:
   0.3s = Snappy, quick
   0.5s = Fast, responsive
   0.8s = Smooth, default
   1.2s = Slow, elegant
   1.5s = Very slow, dramatic
*/

/* Easing options (replace the cubic-bezier):
   ease - Default easing
   ease-in - Starts slow, ends fast
   ease-out - Starts fast, ends slow
   ease-in-out - Starts slow, fast in middle, slow end
   linear - Constant speed
   cubic-bezier(0.68, -0.55, 0.265, 1.55) - Bounce effect (current)
*/


<!-- ============================================ -->
<!-- 9. CHANGE BACKGROUND GRADIENT -->
<!-- ============================================ -->

/* In styles.css, find: */
html, body {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

/* Change to your gradient: */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
background: linear-gradient(135deg, #12c2e9 0%, #c471ed 50%, #f64f59 100%);


<!-- ============================================ -->
<!-- 10. CHANGE BORDER RADIUS (ROUNDED CORNERS) -->
<!-- ============================================ -->

/* In styles.css, find .carousel-item: */
.carousel-item {
    border-radius: 40px;  /* <-- Change this */
}

/* And .image-frame: */
.image-frame {
    border-radius: 50%;  /* <-- Or change this (50% = perfect circle) */
}

/* Options:
   20px = Slightly rounded
   40px = Nicely rounded (default)
   60px = Very rounded
   50% = Perfect circle
*/


<!-- ============================================ -->
<!-- COMPLETE EXAMPLE - CUSTOM CAROUSEL -->
<!-- ============================================ -->

<!--
Here's a complete customized example you can copy:
-->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Custom 3D Carousel</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="carousel-wrapper">
            <div class="carousel-content">
                <div class="carousel-items">
                    <!-- Item 1 -->
                    <div class="carousel-item" style="--bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <div class="item-inner">
                            <div class="image-frame">
                                <img src="https://your-image-1.jpg" alt="Product 1">
                            </div>
                        </div>
                    </div>
                    <!-- Item 2 -->
                    <div class="carousel-item" style="--bg-color: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <div class="item-inner">
                            <div class="image-frame">
                                <img src="https://your-image-2.jpg" alt="Product 2">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="carousel-nav">
                    <button class="nav-btn prev">← </button>
                    <button class="nav-btn next">→</button>
                </div>

                <div class="carousel-dots">
                    <button class="dot active" data-index="0"></button>
                    <button class="dot" data-index="1"></button>
                </div>
            </div>

            <div class="info-panel">
                <h1 class="title">My Products</h1>
                <p class="subtitle">Check out my amazing collection</p>
                <div class="stats">
                    <div class="stat">
                        <span class="label">Products</span>
                        <span class="value">50+</span>
                    </div>
                    <div class="stat">
                        <span class="label">Customers</span>
                        <span class="value">10K+</span>
                    </div>
                </div>
                <button class="cta-button">Shop Now</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>

<!-- ============================================ -->
<!-- NEED HELP? -->
<!-- ============================================ -->

/*
Gradient Generator: https://coolors.co or https://www.gradientos.app/
Image Hosting: https://imgur.com or https://imgbb.com (free)
Color Picker: https://htmlcolorcodes.com
Easing Functions: https://easings.net
*/
