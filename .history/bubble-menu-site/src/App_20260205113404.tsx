import { useEffect, useState } from 'react';
import './App.css';
import BubbleMenu from './components/BubbleMenu/BubbleMenu';
import Prism from './components/Prism/Prism';

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
              Это страстные и увлеченные своей работой члены команды «Phoenix LBSU». Наша команда объединяет экспертов в области программирования, моделирования, дизайна, проектирования и работы с сообществом для создания инновационных решений в области робототехники.
              </p>
              <div className="section-card">
                <h3 className="card-title">Ядро команды</h3>
                <p className="card-text">
                  В дальнейшем сюда можно добавить карточки участников, роли и ссылки на профили.
                </p>
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
