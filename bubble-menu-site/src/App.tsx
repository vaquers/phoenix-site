import { useEffect, useState } from 'react';
import './App.css';
import BubbleMenu from './components/BubbleMenu/BubbleMenu';
import ContactsMap from './components/ContactsMap/ContactsMap';
import DotGrid from './components/DotGrid/DotGrid';
import GradualBlur from './components/GradualBlur/GradualBlur';
import InfiniteMenu, { type MenuItem as BlogItem } from './components/InfiniteMenu/InfiniteMenu';
import Sponsors, { type SponsorItem } from './components/Sponsors';
import TelegramPost from './components/TelegramPost/TelegramPost';
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

type AboutInfo = {
  description: string;
  yearsInCompetitions: number;
  teamSize: number;
};

type ContactsPageData = {
  description: string;
  email: string;
  phone: string;
  address: string;
  telegram: string;
};

type CommunityPost = {
  post_id: number;
  link: string;
  title: string;
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
const JOIN_PAGE_DESCRIPTION =
  'Присоединяйтесь к сообществу, чтобы учиться новому, делиться опытом и создавать полезные проекты вместе.';
const BLOG_DESCRIPTION =
  'Блог команды Phoenix — здесь мы делимся закулисьем подготовки, выступлений и жизни команды.';
const SPONSORS_DESCRIPTION =
  'Наши партнёры помогают развивать инфраструктуру, поддерживают участие в соревнованиях и образовательные инициативы команды Phoenix.';
const CONTACTS_PAGE: ContactsPageData = {
  description: 'Свяжитесь с нами по почте, телефону или в Telegram.',
  email: 'contact@phoenixlbsu.com',
  phone: '+375 (29) 811-10-10',
  address: 'Лицей БГУ, Ульяновская 8, Минск, Беларусь',
  telegram: '@phoenixfromlbsu'
};

const BLOG_PHOTO_FILES = [
  'photo_2026-02-06 23.46.13.jpeg',
  'photo_2026-02-06 23.46.21.jpeg',
  'photo_2026-02-06 23.46.24.jpeg',
  'photo_2026-02-06 23.46.34.jpeg',
  'photo_2026-02-06 23.46.37.jpeg',
  'photo_2026-02-06 23.46.51.jpeg',
  'photo_2026-02-06 23.46.59.jpeg',
  'photo_2026-02-06 23.47.03.jpeg',
  'photo_2026-02-06 23.47.14.jpeg',
  'photo_2026-02-06 23.47.22.jpeg',
  'photo_2026-02-06 23.47.25.jpeg',
  'photo_2026-02-06 23.47.31.jpeg',
  'photo_2026-02-06 23.47.46.jpeg',
  'photo_2026-02-06 23.47.53.jpeg',
  'photo_2026-02-06 23.48.08.jpeg',
  'photo_2026-02-06 23.48.11.jpeg',
  'photo_2026-02-06 23.48.20.jpeg'
];

const BLOG_POSTS: BlogItem[] = BLOG_PHOTO_FILES.map((file, index) => ({
  image: `/photos/${encodeURIComponent(file)}`,
  link: '#',
  title: `Запись ${String(index + 1).padStart(2, '0')}`,
  description: 'Фото из жизни команды Phoenix.'
}));

const SPONSORS: SponsorItem[] = [
  {
    image: '/sponsors/gold.jpeg',
    name: 'Золотой партнёр',
    description: 'Ключевой партнёр, поддерживающий развитие команды и участие в соревнованиях.',
    rank: 1
  },
  {
    image: '/sponsors/silver.png',
    name: 'Серебряный партнёр',
    description: 'Помогает с ресурсами и образовательными инициативами Phoenix.',
    rank: 2
  },
  {
    image: '/sponsors/bronze.png',
    name: 'Бронзовый партнёр',
    description: 'Поддержка мероприятий, логистики и роста нашей команды.',
    rank: 3
  },
  {
    image: '/sponsors/images.jpeg',
    name: 'Партнёр сообщества',
    description: 'Вместе развиваем инженерное сообщество и делимся знаниями.'
  }
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
  const [joinSubmitted, setJoinSubmitted] = useState(false);
  const [joinPageDescription] = useState<string>(JOIN_PAGE_DESCRIPTION);
  const [joinFullName, setJoinFullName] = useState('');
  const [joinGrade, setJoinGrade] = useState('');
  const [joinProfile, setJoinProfile] = useState('');
  const [joinEmail, setJoinEmail] = useState('');
  const [joinTelegram, setJoinTelegram] = useState('');
  const [joinRole, setJoinRole] = useState('');
  const [joinExperience, setJoinExperience] = useState('');
  const [joinMotivation, setJoinMotivation] = useState('');
  const [aboutInfo] = useState<AboutInfo>({
    description:
      'От идеи — к результату. Мы первая беларуская команда Лиги Инженеров из Лицея БГУ! Создаем роботов сообща и вместе ищем нестандартные решения!',
    yearsInCompetitions: YEARS_IN_COMPETITIONS,
    teamSize: teamCards.length
  });
  const [teamDescription] = useState<string>(
    'Это страстные и увлечённые своей работой участники команды «Phoenix LBSU». Мы соединяем экспертизу в программировании, моделировании, дизайне, проектировании и работе с сообществом, чтобы создавать инновационные решения в области робототехники.'
  );
  const [teamMembers] = useState<TeamCard[]>(teamCards);
  const [blogDescription] = useState<string>(BLOG_DESCRIPTION);
  const [blogPosts] = useState<BlogItem[]>(BLOG_POSTS);
  const [sponsorsDescription] = useState<string>(SPONSORS_DESCRIPTION);
  const [sponsors] = useState<SponsorItem[]>(SPONSORS);
  const [contactsPage] = useState<ContactsPageData>(CONTACTS_PAGE);
  const [contactFormSent, setContactFormSent] = useState<boolean | null>(null);
  const [contactFormName, setContactFormName] = useState('');
  const [contactFormEmail, setContactFormEmail] = useState('');
  const [contactFormTelegram, setContactFormTelegram] = useState('');
  const [contactFormMessage, setContactFormMessage] = useState('');
  const [communityPosts] = useState<CommunityPost[]>([
    { post_id: 120, link: 'https://t.me/phoenixlbsu/120', title: 'Phoenix LBSU' }
  ]);
  const uptime = useProjectUptime();

  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setContactFormSent(null);
    setContactFormSent(true);
    setContactFormName('');
    setContactFormEmail('');
    setContactFormTelegram('');
    setContactFormMessage('');
  };

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
                {aboutInfo.description}
              </p>

              <div className="about-stats" role="group" aria-label="Ключевые показатели">
                <div className="about-block">
                  <div className="about-block-image">
                    <img src="/symbols/Trophey_3D.png" alt="" />
                  </div>
                  <span className="about-block-value">{aboutInfo.yearsInCompetitions}</span>
                  <span className="about-block-label">года в соревнованиях</span>
                </div>
                <div className="about-block">
                  <div className="about-block-image">
                    <img src="/symbols/Heart_3D.png" alt="" />
                  </div>
                  <span className="about-block-value">{aboutInfo.teamSize}</span>
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
              <p className="section-text">{teamDescription}</p>
              <div className="team-grid">
                {teamMembers.map(card => (
                  <TiltedCard
                    key={card.caption + card.name}
                    imageSrc={card.imageSrc || '/symbols/person.2.svg'}
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
                {blogDescription || 'Раздел для заметок о технологиях, разборов решений и новостей сообщества.'}
              </p>
              <div className="blog-infinite-wrap" style={{ height: '600px', position: 'relative' }}>
                {blogPosts.length > 0 ? (
                  <InfiniteMenu items={blogPosts} scale={1} />
                ) : (
                  <p className="section-text" style={{ opacity: 0.8 }}>Записей пока нет.</p>
                )}
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
                {sponsorsDescription}
              </p>
              <Sponsors items={sponsors} />
            </div>
          </section>
        );
      case 'contacts':
        return (
          <section id="contacts" className="section">
            <div className="container">
              <h2 className="section-title">Контакты</h2>
              <p className="section-text">
                {contactsPage.description}
              </p>

              <div className="contacts-grid">
                <div className="contacts-column contacts-column-left">
                  <img src="/symbols/message.png" alt="" className="contacts-hero-image" aria-hidden />
                  <div className="contacts-left-cards">
                    <div className="contact-card contacts-form-wrap">
                      <h3 className="contacts-form-title">Напишите — и мы свяжемся с вами!</h3>
                      <form className="contact-form" onSubmit={handleContactSubmit}>
                        <label className="contact-form-label">
                          Фамилия Имя <span className="contact-form-required">*</span>
                          <input type="text" className="contact-form-input" placeholder="Иван Иванов" required value={contactFormName} onChange={(e) => setContactFormName(e.target.value)} />
                        </label>
                        <label className="contact-form-label">
                          Электронная почта <span className="contact-form-required">*</span>
                          <input type="email" className="contact-form-input" placeholder="youremail@phoenix.com" required value={contactFormEmail} onChange={(e) => setContactFormEmail(e.target.value)} />
                        </label>
                        <label className="contact-form-label">
                          Telegram
                          <input type="text" className="contact-form-input" placeholder="@username" value={contactFormTelegram} onChange={(e) => setContactFormTelegram(e.target.value)} />
                        </label>
                        <label className="contact-form-label">
                          Сообщение <span className="contact-form-required">*</span>
                          <textarea className="contact-form-input contact-form-textarea" placeholder="Расскажите нам больше о..." rows={4} required value={contactFormMessage} onChange={(e) => setContactFormMessage(e.target.value)} />
                        </label>
                        {contactFormSent === true && <p className="contact-form-success">Сообщение отправлено. Мы свяжемся с вами!</p>}
                        {contactFormSent === false && <p className="contact-form-error">Не удалось отправить. Попробуйте позже.</p>}
                        <button type="submit" className="contact-form-submit">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
                          Отправить
                        </button>
                      </form>
                    </div>
                    <div className="contact-card contact-card-combined">
                      <h3 className="contact-card-title">Контакты</h3>
                      <div className="contact-card-values">
                        <span className="contact-card-value-row">
                          <img src="/symbols/envelope.svg" alt="" className="contact-card-value-icon" aria-hidden />
                          {contactsPage.email ? (
                            <a href={`mailto:${contactsPage.email}`} className="contact-card-value">{contactsPage.email}</a>
                          ) : (
                            <span className="contact-card-value">—</span>
                          )}
                        </span>
                        <span className="contact-card-value-row">
                          <img src="/symbols/phone.fill.svg" alt="" className="contact-card-value-icon" aria-hidden />
                          {contactsPage.phone ? (
                            <a href={`tel:${contactsPage.phone.replace(/\s/g, '')}`} className="contact-card-value">{contactsPage.phone}</a>
                          ) : (
                            <span className="contact-card-value">—</span>
                          )}
                        </span>
                        <span className="contact-card-value-row">
                          <img src="/symbols/paperplane.fill.svg" alt="" className="contact-card-value-icon" aria-hidden />
                          {contactsPage.telegram ? (
                            <a href={`https://t.me/${contactsPage.telegram.replace('@', '')}`} className="contact-card-value" target="_blank" rel="noopener noreferrer">{contactsPage.telegram}</a>
                          ) : (
                            <span className="contact-card-value">—</span>
                          )}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="contacts-column contacts-column-right">
                  <img src="/symbols/map.png" alt="" className="contacts-hero-image" aria-hidden />
                  <div className="contact-card contact-card-with-map">
                    <h3 className="contact-card-title">Мы находимся тут</h3>
                    <p className="contact-card-value">{contactsPage.address || '—'}</p>
                    <div className="contact-card-map">
                      <ContactsMap />
                    </div>
                  </div>
                </div>
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
              <div className="community-telegram-wrap">
                {communityPosts.length > 0 ? (
                  communityPosts.map((p) => (
                    <div key={p.post_id} className="community-telegram-post">
                      <TelegramPost
                        post={`phoenixlbsu/${p.post_id}`}
                        width="100%"
                        dark={1}
                      />
                    </div>
                  ))
                ) : (
                  <div className="community-telegram-post">
                    <TelegramPost post="phoenixlbsu/120" width="100%" dark={1} />
                  </div>
                )}
              </div>
            </div>
          </section>
        );
      case 'join':
        return (
          <section id="join" className="section">
            <div className="container">
              <h2 className="section-title">Стать участником</h2>
              <p className="section-text">
                {joinPageDescription}
              </p>
              <div className="join-form-card">
                {joinSubmitted ? (
                  <div className="contact-form join-form join-form-success">
                    <h3 className="join-success-title">Ты с нами!</h3>
                    <p className="join-success-text">
                      Спасибо! Мы получили твою заявку и скоро свяжемся с тобой. Жди вестей — впереди много интересного.
                    </p>
                  </div>
                ) : (
                  <form
                    className="contact-form join-form"
                    onSubmit={(e) => {
                      e.preventDefault();
                      setJoinSubmitted(true);
                      setJoinFullName('');
                      setJoinGrade('');
                      setJoinProfile('');
                      setJoinEmail('');
                      setJoinTelegram('');
                      setJoinRole('');
                      setJoinExperience('');
                      setJoinMotivation('');
                    }}
                  >
                    <label className="contact-form-label">
                      ФИО <span className="contact-form-required">*</span>
                      <input
                        type="text"
                        className="contact-form-input"
                        placeholder="Введите ФИО"
                        required
                        value={joinFullName}
                        onChange={(e) => setJoinFullName(e.target.value)}
                      />
                    </label>
                    <div className="join-form-row">
                      <label className="contact-form-label">
                        Параллель <span className="contact-form-required">*</span>
                        <select
                          className="contact-form-input contact-form-select"
                          required
                          value={joinGrade}
                          onChange={(e) => setJoinGrade(e.target.value)}
                        >
                          <option value="">Выбери параллель</option>
                          <option value="10">10</option>
                          <option value="11">11</option>
                        </select>
                      </label>
                      <label className="contact-form-label">
                        Профиль <span className="contact-form-required">*</span>
                        <select
                          className="contact-form-input contact-form-select"
                          required
                          value={joinProfile}
                          onChange={(e) => setJoinProfile(e.target.value)}
                        >
                          <option value="">Выбери профиль</option>
                          <option value="gum">ГУМ</option>
                          <option value="fil">ФИЛ</option>
                          <option value="ist">ИСТ</option>
                          <option value="gram">ГРАМ</option>
                          <option value="eg">ЭГ</option>
                          <option value="bio">БИО</option>
                          <option value="him">ХИМ</option>
                          <option value="m">М</option>
                          <option value="im">ИМ</option>
                          <option value="f">Ф</option>
                          <option value="if">ИФ</option>
                        </select>
                      </label>
                    </div>
                    <div className="join-form-row join-form-row-aligned">
                      <label className="contact-form-label" htmlFor="join-email">
                        Email <span className="contact-form-required">*</span>
                      </label>
                      <label className="contact-form-label" htmlFor="join-telegram">
                        Телеграмм
                      </label>
                      <input
                        id="join-email"
                        type="email"
                        className="contact-form-input"
                        placeholder="your.email@example.com"
                        required
                        value={joinEmail}
                        onChange={(e) => setJoinEmail(e.target.value)}
                      />
                      <input
                        id="join-telegram"
                        type="text"
                        className="contact-form-input"
                        placeholder="@username"
                        value={joinTelegram}
                        onChange={(e) => setJoinTelegram(e.target.value)}
                      />
                    </div>
                    <label className="contact-form-label">
                      Роль / Позиция <span className="contact-form-required">*</span>
                      <select
                        className="contact-form-input contact-form-select"
                        required
                        value={joinRole}
                        onChange={(e) => setJoinRole(e.target.value)}
                      >
                        <option value="">Выбери роль...</option>
                        <option value="programmer">Программист</option>
                        <option value="engineer">Инженер-моделлер</option>
                        <option value="design">Дизайн</option>
                        <option value="media">Медиа &amp; Маркетинг</option>
                        <option value="other">Другое</option>
                      </select>
                    </label>
                    <label className="contact-form-label">
                      Расскажи про свой опыт! <span className="contact-form-required">*</span>
                      <textarea
                        className="contact-form-input contact-form-textarea"
                        placeholder="Расскажи про соревнования, проекты, чем тебе нравится заниматься. Если ты новичок, то просто оставь пару слов о себе :)"
                        rows={4}
                        required
                        value={joinExperience}
                        onChange={(e) => setJoinExperience(e.target.value)}
                      />
                    </label>
                    <label className="contact-form-label">
                      Мотивация и стремления <span className="contact-form-required">*</span>
                      <textarea
                        className="contact-form-input contact-form-textarea"
                        placeholder="Расскажи немного почему ты хочешь попасть в команду, чем ты хочешь тут заниматься, чего хочешь достичь или может о своих идеях для команды"
                        rows={4}
                        required
                        value={joinMotivation}
                        onChange={(e) => setJoinMotivation(e.target.value)}
                      />
                    </label>
                    <button type="submit" className="contact-form-submit">
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        aria-hidden
                      >
                        <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                      </svg>
                      Отправить
                    </button>
                  </form>
                )}
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

      <GradualBlur
        target="page"
        position="bottom"
        height="7rem"
        strength={2}
        divCount={5}
        curve="bezier"
        exponential
        opacity={1}
      />

      <a
        href="#contacts"
        className="sponsor-cta-fixed primary-button"
        aria-label="Стать спонсором — перейти к контактам"
      >
        Стать спонсором
      </a>
      </div>
    </div>
  );
}

export default App;
