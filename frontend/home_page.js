import { useNavigate } from 'react-router-dom';
import './Home.css';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <header className="header">
        <h1>Кредитный скоринг</h1>
        <p>Узнайте вероятность одобрения кредита за 2 минуты</p>
      </header>

      <main className="main-content">
        <div className="features">
          <div className="feature-card">
            <h3>Быстро</h3>
            <p>Результат за 30 секунд</p>
          </div>
          <div className="feature-card">
            <h3>Прозрачно</h3>
            <p>Объяснение решения</p>
          </div>
        </div>

        <button 
          className="cta-button"
          onClick={() => navigate('/consent')}
        >
          Начать
        </button>
      </main>
    </div>
  );
}