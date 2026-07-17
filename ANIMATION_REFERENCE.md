# FocusMirror UI - CSS Animation Reference Guide

## All Custom Keyframe Animations

### 1. Fade In Animation
```css
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}
/* Used for: Overlays, backdrop, smooth opacity changes */
/* Duration: 0.5s ease */
```

### 2. Fade In Up Animation
```css
@keyframes fadeInUp {
  0% { 
    opacity: 0; 
    transform: translateY(20px); 
  }
  100% { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
/* Used for: Cards, sections, main content entrance */
/* Duration: 0.6s ease | Staggered: 0.1s - 1.1s */
```

### 3. Slide Down Animation
```css
@keyframes slideDown {
  0% { 
    opacity: 0; 
    transform: translateY(-20px); 
  }
  100% { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
/* Used for: Top bar, notifications, dropdown menus */
/* Duration: 0.4s ease */
```

### 4. Slide Up Animation
```css
@keyframes slideUp {
  0% { 
    opacity: 0; 
    transform: translateY(30px); 
  }
  100% { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
/* Used for: Modals, overlays, break screen */
/* Duration: 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) */
```

### 5. Bounce Animation
```css
@keyframes bounce {
  0%, 100% { 
    transform: translateY(0); 
  }
  50% { 
    transform: translateY(-12px); 
  }
}
/* Used for: Icon bouncing, attention grabbers */
/* Duration: 2s ease-in-out infinite */
```

### 6. Float Animation
```css
@keyframes float {
  0%, 100% { 
    transform: translateY(0px); 
  }
  50% { 
    transform: translateY(-8px); 
  }
}
/* Used for: Emotion card icons, floating elements */
/* Duration: 3s ease-in-out infinite */
```

### 7. Shimmer Animation
```css
@keyframes shimmer {
  0% { 
    transform: translateX(-100%); 
  }
  100% { 
    transform: translateX(100%); 
  }
}
/* Used for: Progress bar fills, loading indicators */
/* Duration: 2s linear infinite */
/* Applied as pseudo-element ::after with gradient */
```

### 8. Spin Animation
```css
@keyframes spin {
  0% { 
    transform: rotate(0deg); 
  }
  100% { 
    transform: rotate(360deg); 
  }
}
/* Used for: Grade circles, spinners */
/* Duration: 3s linear infinite */
```

### 9. Pulse Animation
```css
@keyframes pulse {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1); 
  }
  50% { 
    opacity: 0.7; 
    transform: scale(1.05); 
  }
}
/* Used for: Earned badges, notifications, live indicators */
/* Duration: 2s ease-in-out infinite */
```

### 10. Alert Pop Animation
```css
@keyframes alertPop {
  0% { 
    opacity: 0; 
    transform: scale(0.9) translateY(10px); 
  }
  100% { 
    opacity: 1; 
    transform: scale(1) translateY(0); 
  }
}
/* Used for: Alert boxes, success messages */
/* Duration: 0.4s ease */
```

### 11. Buddy Pulse Animation
```css
@keyframes buddy-pulse {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(74, 158, 239, 0.6); 
  }
  50% { 
    box-shadow: 0 0 0 12px rgba(74, 158, 239, 0); 
  }
}
/* Used for: Buddy mode FAB button when active */
/* Duration: 2s ease-in-out infinite */
```

### 12. Blink Animation
```css
@keyframes blink {
  0%, 100% { 
    opacity: 1; 
  }
  50% { 
    opacity: 0.3; 
  }
}
/* Used for: Live indicator dot in buddy mode */
/* Duration: 1s ease-in-out infinite */
```

---

## Global Transition Properties

### Standard Card Transition
```css
transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
```
**Used on**: Cards, buttons, containers  
**Effect**: Bouncy, natural-feeling transition  
**Cubic-bezier explanation**: Creates slight overshoot (bouncy effect)

### Smooth State Transition
```css
transition: all 0.3s ease;
```
**Used on**: Form inputs, typography changes  
**Effect**: Smooth, linear acceleration

### Fast Transition
```css
transition: transform 0.2s ease, box-shadow 0.2s ease;
```
**Used on**: Quick interactions, hovers  
**Effect**: Snappy, responsive feel

### Slow Transition
```css
transition: width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
```
**Used on**: Progress bar fills  
**Effect**: Smooth, animated progress visualization

---

## Hover State Effects

### Card Hover
```css
.card:hover {
  transform: translateY(-4px);
  border-color: rgba(29, 158, 117, 0.5);
  box-shadow: 0 8px 24px rgba(29, 158, 117, 0.15);
}
```

### Button Hover
```css
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(29, 158, 117, 0.4);
}
```

### Leaderboard Row Hover
```css
.leaderboard-row:hover {
  background: rgba(29, 158, 117, 0.1);
  transform: translateX(4px);
}
```

### Input Focus
```css
input:focus {
  border-color: #1D9E75;
  box-shadow: 0 0 12px rgba(29, 158, 117, 0.2);
  background: rgba(26, 26, 26, 1);
}
```

---

## Animation Staggering Strategy

Elements are given different animation delays for sequential entrance:

```css
/* First element - immediate start */
animation: fadeInUp 0.6s ease 0.1s both;

/* Second element - 0.1s delay */
animation: fadeInUp 0.6s ease 0.2s both;

/* Third element - 0.2s delay */
animation: fadeInUp 0.6s ease 0.3s both;

/* Pattern continues... */
animation: fadeInUp 0.6s ease 0.Xs both;  /* where X increments */
```

**Result**: Cascading entrance effect for professional appearance

---

## Performance Tips

### GPU-Accelerated Properties
✅ Use these for smooth animations:
- `transform` (translate, scale, rotate, skew)
- `opacity`
- `filter`

### Avoid These (Trigger Reflows)
❌ Don't animate these:
- `width`, `height`
- `top`, `left`, `bottom`, `right`
- `margin`, `padding`
- `border`

### Optimize for Mobile
```css
/* Reduce animation on lower-end devices */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Color Gradients Used

### Primary Button Gradient
```css
background: linear-gradient(135deg, #1D9E75 0%, #15a969 100%);
```

### Body Background Gradient
```css
background: linear-gradient(135deg, #0a0a0a 0%, #0d1b15 50%, #0a0a0a 100%);
```

### Card Background Gradient
```css
background: linear-gradient(135deg, #0d1b15 0%, #111 100%);
```

### Secondary Button Gradient
```css
background: linear-gradient(135deg, #1a1a1a 0%, #222 100%);
```

### Shimmer Gradient (on ::after pseudo-element)
```css
background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
```

### Progress Bar Track Gradient
```css
background: linear-gradient(90deg, rgba(29, 158, 117, 0.05) 0%, rgba(29, 158, 117, 0.02) 100%);
```

---

## Animation Timing Functions Explained

| Function | Effect | Use Case |
|----------|--------|----------|
| `ease` | Slow start/end, fast middle | General transitions |
| `ease-in` | Slow start, fast end | Closing animations |
| `ease-out` | Fast start, slow end | Opening animations |
| `ease-in-out` | Slow start/end, fast middle | Visibility changes |
| `linear` | Constant speed | Spinners, continuous loops |
| `cubic-bezier(0.34, 1.56, 0.64, 1)` | Custom bouncy curve | Natural, playful feel |

---

## Implementation Checklist

When adding new animations:

- [ ] Choose appropriate timing function
- [ ] Set duration (0.2s-1s for interactions, 2-3s for infinite)
- [ ] Add stagger delay if multiple elements
- [ ] Use GPU-accelerated properties (transform, opacity)
- [ ] Test on mobile devices
- [ ] Verify accessibility (consider prefers-reduced-motion)
- [ ] Check performance with DevTools

---

**Last Updated**: 2026-07-18  
**Version**: 1.0 Animation Reference
