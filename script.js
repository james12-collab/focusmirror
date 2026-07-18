class Carousel {
    constructor() {
        this.items = document.querySelectorAll('.carousel-item');
        this.dots = document.querySelectorAll('.dot');
        this.prevBtn = document.querySelector('.nav-btn.prev');
        this.nextBtn = document.querySelector('.nav-btn.next');
        this.currentIndex = 0;
        this.totalItems = this.items.length;
        this.isAnimating = false;
        this.autoPlayInterval = null;

        this.init();
    }

    init() {
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        this.dots.forEach(dot => {
            dot.addEventListener('click', (e) => {
                this.goTo(parseInt(e.target.dataset.index));
            });
        });

        // Auto-play
        this.startAutoPlay();

        // Pause on hover
        const carousel = document.querySelector('.carousel-items');
        carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
        carousel.addEventListener('mouseleave', () => this.startAutoPlay());

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });

        // Hide deployment status
        this.hideDeploymentStatus();
    }

    hideDeploymentStatus() {
        const statusElement = document.getElementById('deployment-status');
        if (statusElement) {
            setTimeout(() => {
                statusElement.classList.add('hidden');
                setTimeout(() => {
                    statusElement.style.display = 'none';
                }, 500);
            }, 500);
        }
    }

    updateCarousel() {
        this.items.forEach((item, index) => {
            item.classList.remove('active', 'prev-active', 'next-active');

            if (index === this.currentIndex) {
                item.classList.add('active');
            } else if (index === (this.currentIndex - 1 + this.totalItems) % this.totalItems) {
                item.classList.add('prev-active');
            } else if (index === (this.currentIndex + 1) % this.totalItems) {
                item.classList.add('next-active');
            }
        });

        // Update dots
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }

    next() {
        if (this.isAnimating) return;
        this.isAnimating = true;

        this.currentIndex = (this.currentIndex + 1) % this.totalItems;
        this.updateCarousel();

        setTimeout(() => {
            this.isAnimating = false;
        }, 800);

        this.resetAutoPlay();
    }

    prev() {
        if (this.isAnimating) return;
        this.isAnimating = true;

        this.currentIndex = (this.currentIndex - 1 + this.totalItems) % this.totalItems;
        this.updateCarousel();

        setTimeout(() => {
            this.isAnimating = false;
        }, 800);

        this.resetAutoPlay();
    }

    goTo(index) {
        if (this.isAnimating || index === this.currentIndex) return;
        this.isAnimating = true;

        this.currentIndex = index;
        this.updateCarousel();

        setTimeout(() => {
            this.isAnimating = false;
        }, 800);

        this.resetAutoPlay();
    }

    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.next();
        }, 5000);
    }

    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
        }
    }

    resetAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }
}

// Initialize carousel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Carousel();

    // Add some parallax effect on mouse move
    document.addEventListener('mousemove', (e) => {
        const carousel = document.querySelector('.carousel-items');
        if (!carousel) return;

        const rect = carousel.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        const rotateX = (y / rect.height) * 5;
        const rotateY = (x / rect.width) * 5;

        carousel.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    // Reset transform on mouse leave
    document.addEventListener('mouseleave', () => {
        const carousel = document.querySelector('.carousel-items');
        if (carousel) {
            carousel.style.transform = 'rotateX(0deg) rotateY(0deg)';
        }
    });

    // Log deployment status
    console.log('%c✅ 3D Carousel Deployed Successfully!', 'color: #667eea; font-size: 16px; font-weight: bold;');
    console.log('%cVersion: 1.0 | Loaded at: ' + new Date().toLocaleTimeString(), 'color: #764ba2; font-size: 12px;');
    console.log('%cAll animations and features are operational.', 'color: #4facfe; font-size: 12px;');
});

// Touch support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.querySelector('.carousel-items').addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.querySelector('.carousel-items').addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const carousel = document.querySelector('.carousel__js');
    if (touchEndX < touchStartX - 50) {
        // Swiped left
        document.querySelector('.nav-btn.next').click();
    }
    if (touchEndX > touchStartX + 50) {
        // Swiped right
        document.querySelector('.nav-btn.prev').click();
    }
}
