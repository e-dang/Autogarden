import $ from 'jquery';

const imageUrls = [
    '/images/markus-spiske-4PG6wLlVag4-unsplash.jpg',
    '/images/markus-spiske-vrbZVyX2k4I-unsplash.jpg',
    '/images/markus-spiske-Yy-dHQP-Ax0-unsplash.jpg',
    '/images/markus-spiske-B-2mkX1rjjY-unsplash.jpg',
    '/images/markus-spiske-IRrUkB8Fq-0-unsplash.jpg',
    '/images/markus-spiske-lq2A2ki2w2Y-unsplash.jpg',
    '/images/markus-spiske-p4lNiLlog8g-unsplash.jpg',
    '/images/markus-spiske-Wnr2ohKUIYw-unsplash.jpg',
];

class ImageRotator {
    constructor(urls = imageUrls, componentSelector = '#mainContent', timeout = 60000) {
        this.prevIdx = null;
        this.urls = urls;
        this.componentSelector = componentSelector;
        this.timeout = timeout;
        this.images = [];
        this._loadImages();
    }

    begin() {
        this._setBackground();
        $(this.componentSelector).addClass('fade-in');
        setInterval(() => {
            this.idx++;
            this._setBackground();
        }, this.timeout);
    }

    _setBackground() {
        $(this.componentSelector).css('background-image', `url(${this.images[this._getIdx()].src})`);
    }

    _loadImages() {
        return new Promise((resolve, reject) => {
            for (let url of this.urls) {
                const image = new Image();
                image.src = url;
                this.images.push(image);
            }
        });
    }

    _getIdx() {
        let idx = -1;
        while (idx == this.prevIdx || idx == -1) {
            idx = Math.round(Math.random() * (this.urls.length - 1));
        }

        this.prevIdx = idx;
        return idx;
    }
}

export default ImageRotator;
