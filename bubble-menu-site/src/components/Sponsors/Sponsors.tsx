import { FC } from 'react';
import './Sponsors.css';

export type SponsorItem = {
  image: string;
  name: string;
  description: string;
  rank?: 1 | 2 | 3;
};

const MEDAL_SRC: Record<1 | 2 | 3, string> = {
  1: '/symbols/gold_medal.png',
  2: '/symbols/silver_medal.png',
  3: '/symbols/bronze_medal.png'
};

type SponsorsProps = {
  items: SponsorItem[];
};

const Sponsors: FC<SponsorsProps> = ({ items }) => {
  return (
    <div className="sponsors-grid">
      {items.map((sponsor, index) =>
        sponsor.rank != null ? (
          <article key={index} className="sponsor-card sponsor-card-top3">
            <div className="sponsor-card-hero">
              {sponsor.image ? (
                <img src={sponsor.image} alt="" className="sponsor-card-photo" />
              ) : (
                <div className="sponsor-card-placeholder">
                  <span className="sponsor-card-placeholder-text">Здесь может быть ваше фото</span>
                </div>
              )}
              <div className="sponsor-card-gradient" aria-hidden />
              <div className="sponsor-medal-wrap">
                <img
                  src={MEDAL_SRC[sponsor.rank]}
                  alt=""
                  className="sponsor-medal-img"
                  aria-hidden
                />
              </div>
            </div>
            <div className="sponsor-card-body">
              <span className="sponsor-card-subtitle">
                {sponsor.rank === 1 ? 'Главный партнёр' : sponsor.rank === 2 ? 'Серебряный партнёр' : 'Бронзовый партнёр'}
              </span>
              <h3 className="sponsor-card-title">{sponsor.name}</h3>
              <p className="sponsor-card-description">{sponsor.description}</p>
            </div>
          </article>
        ) : (
          <article key={index} className="sponsor-card sponsor-card-regular">
            <div className="sponsor-card-hero">
              {sponsor.image ? (
                <img src={sponsor.image} alt="" className="sponsor-card-photo" />
              ) : (
                <div className="sponsor-card-placeholder">
                  <span className="sponsor-card-placeholder-text">Здесь может быть ваше фото</span>
                </div>
              )}
              <div className="sponsor-card-gradient" aria-hidden />
            </div>
            <div className="sponsor-card-body">
              <h3 className="sponsor-card-title">{sponsor.name}</h3>
              <p className="sponsor-card-description">{sponsor.description}</p>
            </div>
          </article>
        )
      )}
    </div>
  );
};

export default Sponsors;
