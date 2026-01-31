import { useEffect, useState } from 'react';

const FAVICONS = [
    '/fav.svg',
    '/icon.svg',
    '/favicon.svg'
];

export function DynamicFavicon() {
    const [index, setIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setIndex((prev) => (prev + 1) % FAVICONS.length);
        }, 5000); // Change every 1 second

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        const link: HTMLLinkElement | null = document.querySelector("link[rel~='icon']");
        if (!link) {
            const newLink = document.createElement('link');
            newLink.rel = 'icon';
            document.head.appendChild(newLink);
            newLink.href = FAVICONS[index];
        } else {
            link.href = FAVICONS[index];
        }
    }, [index]);

    return null;
}
