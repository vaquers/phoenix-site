import { useEffect, useState } from 'react';
import './App.css';
import BubbleMenu from './components/BubbleMenu/BubbleMenu';
import Prism from './components/Prism/Prism';
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
  overlay: string;
};

const menuItems: MenuItem[] = [
  {
    label: 'про нас',
    href: '#about',
    ariaLabel: 'Перейти к разделу Про нас',
    rotation: -8,
    hoverStyles: { bgColor: '#2563eb', textColor: '#ffffff' }
  },
  {
    label: 'команда',
    href: '#team',
    ariaLabel: 'Перейти к разделу Команда',
    rotation: 8,
    hoverStyles: { bgColor: '#059669', textColor: '#ffffff' }
  },
  {
    label: 'блог',
    href: '#blog',
    ariaLabel: 'Перейти к разделу Блог',
    rotation: -8,
    hoverStyles: { bgColor: '#f97316', textColor: '#111827' }
  },
  {
    label: 'спонсоры',
    href: '#sponsors',
    ariaLabel: 'Перейти к разделу Спонсоры',
    rotation: 8,
    hoverStyles: { bgColor: '#ec4899', textColor: '#ffffff' }
  },
  {
    label: 'контакты',
    href: '#contacts',
    ariaLabel: 'Перейти к разделу Контакты',
    rotation: -8,
    hoverStyles: { bgColor: '#6366f1', textColor: '#ffffff' }
  },
  {
    label: 'сообщество',
    href: '#community',
    ariaLabel: 'Перейти к разделу Сообщество',
    rotation: 8,
    hoverStyles: { bgColor: '#14b8a6', textColor: '#022c22' }
  },
  {
    label: 'стать участником',
    href: '#join',
    ariaLabel: 'Перейти к разделу Стать участником',
    rotation: -8,
    hoverStyles: { bgColor: '#0f766e', textColor: '#ecfeff' }
  }
];

const teamCards: TeamCard[] = [
  {
    imageSrc: 'https://i.scdn.co/image/ab67616d0000b273d9985092cd88bffd97653b58',
    altText: 'Phoenix Core Team',
    caption: 'Phoenix Core Team',
    overlay: 'Phoenix Core Team'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg',
    altText: 'Software Squad',
    caption: 'Software Squad',
    overlay: 'Software Squad'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg',
    altText: 'ML & Simulation',
    caption: 'ML & Simulation',
    overlay: 'ML & Simulation'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3861964/pexels-photo-3861964.jpeg',
    altText: 'Product & Design',
    caption: 'Product & Design',
    overlay: 'Product & Design'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/1181467/pexels-photo-1181467.jpeg',
    altText: 'Hardware & Control',
    caption: 'Hardware & Control',
    overlay: 'Hardware & Control'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/1181533/pexels-photo-1181533.jpeg',
    altText: 'Frontend & UX',
    caption: 'Frontend & UX',
    overlay: 'Frontend & UX'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3862383/pexels-photo-3862383.jpeg',
    altText: 'Backend & Data',
    caption: 'Backend & Data',
    overlay: 'Backend & Data'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/1181243/pexels-photo-1181243.jpeg',
    altText: 'Community & Ops',
    caption: 'Community & Ops',
    overlay: 'Community & Ops'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg',
    altText: 'Research & Experiments',
    caption: 'Research & Experiments',
    overlay: 'Research & Experiments'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3861958/pexels-photo-3861958.jpeg',
    altText: 'Education & Outreach',
    caption: 'Education & Outreach',
    overlay: 'Education & Outreach'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3861817/pexels-photo-3861817.jpeg',
    altText: 'Infrastructure',
    caption: 'Infrastructure',
    overlay: 'Infrastructure'
  },
  {
    imageSrc: 'https://images.pexels.com/photos/3861968/pexels-photo-3861968.jpeg',
    altText: 'Partners & Sponsors',
    caption: 'Partners & Sponsors',
    overlay: 'Partners & Sponsors'
  }
];

function getSectionFromHash(hash: string): SectionId {
  const clean = hash.replace('#', '') as SectionId;
  const allowed: SectionId[] = ['about', 'team', 'blog', 'sponsors', 'contacts', 'community', 'join'];
  return allowed.includes(clean) ? clean : 'about';
}

function App() {
  const [currentSection, setCurrentSection] = useState<SectionId>(() =>
    typeof window !== 'undefined' ? getSectionFromHash(window.location.hash || '#about') : 'about'
  );

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
          <section id="about" className="section">
            <div className="container">
              <h2 className="section-title">Про нас</h2>
              <p className="section-text">
                Мы собираем людей, которым интересны современные веб-технологии, открытые проекты и обмен опытом.
              </p>
              <div className="section-card">
                <h3 className="card-title">Кто мы</h3>
                <p className="card-text">
                  Здесь вы можете кратко описать миссию, ценности и формат вашего сообщества или проекта.
                </p>
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
                    showTooltip
                    displayOverlayContent
                    overlayContent={<p className="tilted-card-overlay-text">{card.overlay}</p>}
                  />
                ))}
              </div>
            </div>
          </section>
        );
      case 'blog':
        return (
          <section id="blog" className="section">
            <div className="container">
              <h2 className="section-title">Блог</h2>
              <p className="section-text">
                Раздел для заметок о технологиях, разборов решений и новостей сообщества.
              </p>
              <div className="section-card">
                <h3 className="card-title">Последние материалы</h3>
                <p className="card-text">
                  Пока здесь заглушка, но позже вы сможете подтягивать записи из CMS, Markdown-файлов или API.
                </p>
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
              <div className="section-card">
                <h3 className="card-title">Партнёрские форматы</h3>
                <p className="card-text">
                  Опишите уровни спонсорства, форматы участия компаний и то, какую ценность они получают.
                </p>
              </div>
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
      <div className="prism-bg" aria-hidden="true">
        <Prism
          animationType="rotate"
          timeScale={0.4}
          height={4.5}
          baseWidth={5.5}
          scale={2.9}
          hueShift={0}
          colorFrequency={1}
          noise={0}
          glow={1}
        />
      </div>
      <div className="app-content">
        <BubbleMenu
        logo={<span style={{ fontWeight: 700 }}>PHOENIX</span>}
        items={menuItems}
        menuAriaLabel="Переключить основное меню навигации"
        menuBg="#ffffff"
        menuContentColor="#111111"
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
