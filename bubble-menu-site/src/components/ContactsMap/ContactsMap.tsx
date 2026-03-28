import { useEffect, useRef } from 'react';
import './ContactsMap.css';

const YANDEX_MAP_SCRIPT_URL =
  'https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3Abaa8e3e3e27a118fed3727990bb8156d115ecfb3b6eea026c527bbeb653ab3e8&width=534&height=430&lang=ru_RU&scroll=true';

export default function ContactsMap() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.charset = 'utf-8';
    script.async = true;
    script.src = YANDEX_MAP_SCRIPT_URL;
    container.appendChild(script);

    return () => {
      if (container.contains(script)) {
        container.removeChild(script);
      }
    };
  }, []);

  return <div ref={containerRef} className="contacts-map" aria-label="Карта" />;
}
