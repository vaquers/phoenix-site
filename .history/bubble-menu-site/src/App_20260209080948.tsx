import { useEffect, useState } from 'react';
import './App.css';
import BubbleMenu from './components/BubbleMenu/BubbleMenu';
import DotGrid from './components/DotGrid/DotGrid';
import InfiniteMenu, { type MenuItem as BlogItem } from './components/InfiniteMenu/InfiniteMenu';
import Sponsors, { type SponsorItem } from './components/Sponsors';
import TiltedCard from './components/TiltedCard/TiltedCard';

type MenuItem = {
  label: string;
  href: string;
  ariaLabel: string;
  rotation: number;
  hoverStyles: {
    bgColor: string;
    textColor: string;
  };
};

type SectionId = 'about' | 'team' | 'blog' | 'sponsors' | 'contacts' | 'community' | 'join';

type TeamCard = {
  imageSrc: string;
  altText: string;
  caption: string;
  name: string;
  role: string;
};

const menuItems: MenuItem[] = [
  {
    label: 'про нас',
    href: '#about',
    ariaLabel: 'Перейти к разделу Про нас',
    rotation: -8,
    hoverStyles: { bgColor: '#0D3B66', textColor: '#ffffff' }
  },
  {
    label: 'команда',
    href: '#team',
    ariaLabel: 'Перейти к разделу Команда',
    rotation: 8,
    hoverStyles: { bgColor: '#EE964B', textColor: '#000000' }
  },
  {
    label: 'блог',
    href: '#blog',
    ariaLabel: 'Перейти к разделу Блог',
    rotation: -8,
    hoverStyles: { bgColor: '#F4D35E', textColor: '#000000' }
  },
  {
    label: 'спонсоры',
    href: '#sponsors',
    ariaLabel: 'Перейти к разделу Спонсоры',
    rotation: 8,
    hoverStyles: { bgColor: '#F95738', textColor: '#ffffff' }
  },
  {
    label: 'контакты',
    href: '#contacts',
    ariaLabel: 'Перейти к разделу Контакты',
    rotation: -8,
    hoverStyles: { bgColor: '#0D3B66', textColor: '#ffffff' }
  },
  {
    label: 'сообщество',
    href: '#community',
    ariaLabel: 'Перейти к разделу Сообщество',
    rotation: 8,
    hoverStyles: { bgColor: '#FAF0CA', textColor: '#0D3B66' }
  },
  {
    label: 'стать участником',
    href: '#join',
    ariaLabel: 'Перейти к разделу Стать участником',
    rotation: -8,
    hoverStyles: { bgColor: '#EE964B', textColor: '#000000' }
  }
];

const teamCards: TeamCard[] = [
  {
    imageSrc: '/avatars/sofa.jpeg',
    altText: 'София Урываева',
    caption: 'София Урываева',
    name: 'София Урываева',
    role: 'Капитан команды\nИнженер-моделлер'
  },
  {
    imageSrc: '/avatars/liza.jpeg',
    altText: 'Лиза Крупец',
    caption: 'Лиза Крупец',
    name: 'Лиза Крупец',
    role: 'Инженер-моделлер'
  },
  {
    imageSrc: '/avatars/anton.jpeg',
    altText: 'Антон Маковский',
    caption: 'Антон Маковский',
    name: 'Антон Маковский',
    role: 'Инженер-моделлер'
  },
  {
    imageSrc: '/avatars/dominik.jpeg',
    altText: 'Доминик Мазуро',
    caption: 'Доминик Мазуро',
    name: 'Доминик Мазуро',
    role: 'Программист'
  },
  {
    imageSrc: '/avatars/agata.jpeg',
    altText: 'Агата Кудрявцева',
    caption: 'Агата Кудрявцева',
    name: 'Агата Кудрявцева',
    role: 'Медиа & Маркетинг'
  },
  {
    imageSrc: '/avatars/kirill.jpeg',
    altText: 'Кирилл Сапего',
    caption: 'Кирилл Сапего',
    name: 'Кирилл Сапего',
    role: 'Программист'
  },
  {
    imageSrc: '/avatars/rodion.jpeg',
    altText: 'Родион Азарёнок',
    caption: 'Родион Азарёнок',
    name: 'Родион Азарёнок',
    role: 'Инженер-моделлер'
  },
  {
    imageSrc: '/avatars/vanya.jpeg',
    altText: 'Иван Трубчик',
    caption: 'Иван Трубчик',
    name: 'Иван Трубчик',
    role: 'Программист & Дизайнер'
  },
  {
    imageSrc: '/avatars/nastya.jpeg',
    altText: 'Настя Говорова',
    caption: 'Настя Говорова',
    name: 'Настя Говорова',
    role: 'Медиа'
  },
  {
    imageSrc: '/avatars/alla.jpeg',
    altText: 'Алла Юнцевич',
    caption: 'Алла Юнцевич',
    name: 'Алла Юнцевич',
    role: 'Инженер-моделлер'
  }
];

const PROJECT_START_DATE = new Date('2024-10-27T00:00:00');
const YEARS_IN_COMPETITIONS = 2;

const sponsorItems: SponsorItem[] = [
  {
    image: '/sponsors/gold.jpeg',
    name: 'Лицей имени Ф.Э. Дзержинского БГУ',
    description: 'Лучшее учериждение обра',
    rank: 1
  },
  {
    image: '/sponsors/silver.png',
    name: 'Технологический спонсор',
    description: 'Предоставляет софт, облачную инфраструктуру и консультации по разработке.',
    rank: 2
  },
  {
    image: '/sponsors/bronze.png',
    name: 'Партнёр соревнований',
    description: 'Участвует в организации региональных этапов и награждении победителей. Станьте бронзовым партнёром команды Phoenix.',
    rank: 3
  },
  {
    image: '',
    name: 'Здесь может быть ваше фото',
    description: 'Сделаем этот мир лучше вместе! Поддержите молодых инженеров и станьте частью нашей истории.'
  },
  {
    image: '',
    name: 'Здесь может быть ваше фото',
    description: 'Сделаем этот мир лучше вместе! Ваша поддержка помогает нам создавать технологии будущего.'
  },
  {
    image: '',
    name: 'Здесь может быть ваше фото',
    description: 'Сделаем этот мир лучше вместе! Присоединяйтесь к партнёрам команды Phoenix.'
  }
];

const blogItems: BlogItem[] = [
  { image: '/photos/photo_2026-02-06 23.46.13.jpeg', link: '#', title: 'Запись 1', description: 'Краткое описание материала блога.' },
  { image: '/photos/photo_2026-02-06 23.46.21.jpeg', link: '#', title: 'Запись 2', description: 'Ещё один пост о технологиях и событиях.' },
  { image: '/photos/photo_2026-02-06 23.46.24.jpeg', link: '#', title: 'Запись 3', description: 'Новости команды и соревнований.' },
  { image: '/photos/photo_2026-02-06 23.46.34.jpeg', link: '#', title: 'Запись 4', description: 'Разбор решений и полезные ссылки.' },
  { image: '/photos/photo_2026-02-06 23.46.37.jpeg', link: '#', title: 'Запись 5', description: 'События и активность команды.' },
  { image: '/photos/photo_2026-02-06 23.46.51.jpeg', link: '#', title: 'Запись 6', description: 'Идеи и проекты.' },
  { image: '/photos/photo_2026-02-06 23.46.59.jpeg', link: '#', title: 'Запись 7', description: 'Материалы и обновления.' },
  { image: '/photos/photo_2026-02-06 23.47.03.jpeg', link: '#', title: 'Запись 8', description: 'Заметки и анонсы.' },
  { image: '/photos/photo_2026-02-06 23.47.14.jpeg', link: '#', title: 'Запись 9', description: 'События сообщества.' },
  { image: '/photos/photo_2026-02-06 23.47.22.jpeg', link: '#', title: 'Запись 10', description: 'Новости и проекты.' },
  { image: '/photos/photo_2026-02-06 23.47.25.jpeg', link: '#', title: 'Запись 11', description: 'Разборы и туториалы.' },
  { image: '/photos/photo_2026-02-06 23.47.31.jpeg', link: '#', title: 'Запись 12', description: 'Практика и опыт.' },
  { image: '/photos/photo_2026-02-06 23.47.46.jpeg', link: '#', title: 'Запись 13', description: 'Идеи и решения.' },
  { image: '/photos/photo_2026-02-06 23.47.53.jpeg', link: '#', title: 'Запись 14', description: 'Анонсы и встречи.' },
  { image: '/photos/photo_2026-02-06 23.48.08.jpeg', link: '#', title: 'Запись 15', description: 'Результаты и планы.' },
  { image: '/photos/photo_2026-02-06 23.48.11.jpeg', link: '#', title: 'Запись 16', description: 'Команда и активность.' },
  { image: '/photos/photo_2026-02-06 23.48.20.jpeg', link: '#', title: 'Запись 17', description: 'Итоги и впечатления.' }
];

function getSectionFromHash(hash: string): SectionId {
  const clean = hash.replace('#', '') as SectionId;
  const allowed: SectionId[] = ['about', 'team', 'blog', 'sponsors', 'contacts', 'community', 'join'];
  return allowed.includes(clean) ? clean : 'about';
}

function useProjectUptime() {
  const [uptime, setUptime] = useState(() => getUptime());
  useEffect(() => {
    const t = setInterval(() => setUptime(getUptime()), 1000);
    return () => clearInterval(t);
  }, []);
  return uptime;
}

function getUptime() {
  const now = new Date();
  const diff = now.getTime() - PROJECT_START_DATE.getTime();
  if (diff < 0) {
    return { years: 0, months: 0, days: 0, hours: 0, minutes: 0, seconds: 0 };
  }
  const seconds = Math.floor(diff / 1000) % 60;
  const minutes = Math.floor(diff / 60000) % 60;
  const hours = Math.floor(diff / 3600000) % 24;
  const totalDays = Math.floor(diff / 86400000);
  const years = Math.floor(totalDays / 365);
  const remainingDays = totalDays - years * 365;
  const months = Math.floor(remainingDays / 30);
  const days = remainingDays % 30;
  return { years, months, days, hours, minutes, seconds };
}

function App() {
  const [currentSection, setCurrentSection] = useState<SectionId>(() =>
    typeof window !== 'undefined' ? getSectionFromHash(window.location.hash || '#about') : 'about'
  );
  const uptime = useProjectUptime();

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentSection(getSectionFromHash(window.location.hash || '#about'));
      window.scrollTo({ top: 0 });
    };

    window.addEventListener('hashchange', handleHashChange);
    // начальное состояние, если пользователь сразу перешёл по ссылке вида /#team
    handleHashChange();

    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const renderSection = () => {
    switch (currentSection) {
      case 'about':
        return (
          <section id="about" className="section about-section">
            <div className="container">
              <h2 className="section-title about-title">Phoenix LBSU <br /> FTC Team #28420</h2>
              <p className="about-intro">
                От идеи — к результату. Мы первая беларуская команда Лиги Инженеров из Лицея БГУ! Создаем роботов сообща и вместе ищем нестандартные решения!
              </p>

              <div className="about-stats" role="group" aria-label="Ключевые показатели">
                <div className="about-block">
                  <div className="about-block-image">
                    <img src="/symbols/Trophey_3D.png" alt="" />
                  </div>
                  <span className="about-block-value">{YEARS_IN_COMPETITIONS}</span>
                  <span className="about-block-label">года в соревнованиях</span>
                </div>
                <div className="about-block">
                  <div className="about-block-image">
                    <img src="/symbols/Heart_3D.png" alt="" />
                  </div>
                  <span className="about-block-value">{teamCards.length}</span>
                  <span className="about-block-label">человек в команде</span>
                </div>
                <div className="about-block about-block-uptime">
                  <div className="about-block-image">
                    <img src="/symbols/Calendar_3D.png" alt="" />
                  </div>
                  <div className="about-uptime" aria-live="polite">
                    <span className="about-uptime-unit"><em>{uptime.years}</em> г</span>
                    <span className="about-uptime-unit"><em>{uptime.months}</em> мес</span>
                    <span className="about-uptime-unit"><em>{uptime.days}</em> д</span>
                    <span className="about-uptime-unit"><em>{String(uptime.hours).padStart(2, '0')}</em> ч</span>
                    <span className="about-uptime-unit"><em>{String(uptime.minutes).padStart(2, '0')}</em> мин</span>
                    <span className="about-uptime-unit"><em>{String(uptime.seconds).padStart(2, '0')}</em> сек</span>
                  </div>
                  <span className="about-block-label">проекту</span>
                </div>
              </div>

              <div className="about-actions">
                <a href="#blog" className="about-btn about-btn-news">
                  Последние новости
                </a>
                <a href="#team" className="about-btn about-btn-team">
                  Наша команда
                </a>
              </div>
            </div>
          </section>
        );
      case 'team':
        return (
          <section id="team" className="section">
            <div className="container">
              <h2 className="section-title">Знакомьтесь с нашей Командой</h2>
              <p className="section-text">
                Это страстные и увлечённые своей работой участники команды «Phoenix LBSU». Мы соединяем экспертизу в
                программировании, моделировании, дизайне, проектировании и работе с сообществом, чтобы создавать
                инновационные решения в области робототехники.
              </p>
              <div className="team-grid">
                {teamCards.map(card => (
                  <TiltedCard
                    key={card.caption}
                    imageSrc={card.imageSrc}
                    altText={card.altText}
                    captionText={card.caption}
                    containerHeight="300px"
                    containerWidth="100%"
                    imageHeight="300px"
                    imageWidth="300px"
                    rotateAmplitude={12}
                    scaleOnHover={1.05}
                    showMobileWarning={false}
                    showTooltip={false}
                    displayOverlayContent
                    overlayContent={
                      <p className="tilted-card-overlay-text">
                        <span className="tilted-card-name">{card.name}</span>
                        <br />
                        {card.role}
                      </p>
                    }
                  />
                ))}
              </div>
            </div>
          </section>
        );
      case 'blog':
        return (
          <section id="blog" className="section section-blog">
            <div className="container">
              <h2 className="section-title">Блог</h2>
              <p className="section-text">
                Раздел для заметок о технологиях, разборов решений и новостей сообщества.
              </p>
              <div className="blog-infinite-wrap" style={{ height: '600px', position: 'relative' }}>
                <InfiniteMenu items={blogItems} scale={1} />
              </div>
            </div>
          </section>
        );
      case 'sponsors':
        return (
          <section id="sponsors" className="section">
            <div className="container">
              <h2 className="section-title">Спонсоры</h2>
              <p className="section-text">
                Поддержка партнёров помогает развивать инфраструктуру и проводить больше активностей для участников.
              </p>
              <Sponsors items={sponsorItems} />
            </div>
          </section>
        );
      case 'contacts':
        return (
          <section id="contacts" className="section">
            <div className="container">
              <h2 className="section-title">Контакты</h2>
              <p className="section-text">
                Здесь можно разместить email, ссылки на чаты и формы обратной связи, чтобы с вами было легко связаться.
              </p>
              <div className="section-card">
                <h3 className="card-title">Связаться с нами</h3>
                <p className="card-text">
                  В будущем этот блок можно заменить реальной формой отправки сообщения или интеграцией с сервисами.
                </p>
              </div>
            </div>
          </section>
        );
      case 'community':
        return (
          <section id="community" className="section">
            <div className="container">
              <h2 className="section-title">Сообщество</h2>
              <p className="section-text">
                Phoenix — это не только сайт, но и живые люди, встречи, дискуссии и совместные проекты.
              </p>
              <div className="section-card">
                <h3 className="card-title">Форматы взаимодействия</h3>
                <p className="card-text">
                  Онлайн-созвоны, митапы, разборы кода и менторство — укажите те активности, которые вы планируете.
                </p>
              </div>
            </div>
          </section>
        );
      case 'join':
        return (
          <section id="join" className="section section-accent">
            <div className="container">
              <h2 className="section-title">Стать участником</h2>
              <p className="section-text">
                Присоединяйтесь к сообществу, чтобы учиться новому, делиться опытом и создавать полезные проекты
                вместе.
              </p>
              <div className="section-card">
                <h3 className="card-title">Следующий шаг</h3>
                <p className="card-text">
                  Добавьте сюда кнопку регистрации, ссылку на форму или инвайт в ваш основной канал общения.
                </p>
                <button className="primary-button" type="button">
                  Оставить заявку
                </button>
              </div>
            </div>
          </section>
        );
      default:
        return null;
    }
  };

  return (
    <div className="app-root">
      <div className="prism-bg" aria-hidden="true" style={{ pointerEvents: 'none' }}>
        <DotGrid
          dotSize={5}
          gap={15}
          baseColor="#0D3B66"
          activeColor="#EE964B"
          proximity={120}
          shockRadius={250}
          shockStrength={5}
          resistance={750}
          returnDuration={2.2}
          style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}
        />
      </div>
      <div className="app-content">
        <BubbleMenu
        logo={<span style={{ fontWeight: 700 }}>PHOENIX</span>}
        items={menuItems}
        menuAriaLabel="Переключить основное меню навигации"
        menuBg="#ffffff"
        menuContentColor="#0D3B66"
        useFixedPosition={true}
        animationEase="back.out(1.5)"
        animationDuration={0.5}
        staggerDelay={0.12}
      />

      <main className="page-main" aria-label="Основной контент">
        {renderSection()}
      </main>
      </div>
    </div>
  );
}

export default App;
