import { useEffect, useRef } from 'react';
import './TelegramPost.css';

const WIDGET_SCRIPT = 'https://telegram.org/js/telegram-widget.js?22';

type TelegramPostProps = {
  post?: string;
  width?: string;
  dark?: 0 | 1;
};

export default function TelegramPost({
  post = 'phoenixlbsu/120',
  width = '100%',
  dark = 1
}: TelegramPostProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const script = document.createElement('script');
    script.async = true;
    script.src = WIDGET_SCRIPT;
    script.setAttribute('data-telegram-post', post);
    script.setAttribute('data-width', width);
    script.setAttribute('data-dark', String(dark));
    container.appendChild(script);

    return () => {
      if (container.contains(script)) {
        container.removeChild(script);
      }
    };
  }, [post, width, dark]);

  return <div ref={containerRef} className="telegram-post" aria-label="Пост из Telegram" />;
}
