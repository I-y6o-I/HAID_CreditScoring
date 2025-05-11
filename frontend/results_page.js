import { useLocation } from 'react-router-dom';
import './Results.css';

export default function Results() {
  const { state } = useLocation();
  const featureImportance = state?.importance || {};

  return (
    <div className="results-container">
      <h2>Результаты анализа</h2>
      
      <div className="prediction-result">
        <h3>Статус: {state?.approved ? 'Одобрено' : 'Отказано'}</h3>
        <p>Вероятность: {state?.probability}%</p>
      </div>

      <div className="feature-importance">
        <h3>Факторы решения:</h3>
        {Object.entries(featureImportance)
          .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
          .map(([feature, value]) => (
            <div key={feature} className="feature-row">
              <span>{feature}</span>
              <div 
                className={`importance-bar ${value > 0 ? 'positive' : 'negative'}`}
                style={{ width: `${Math.abs(value) * 50}%` }}
              >
                {value.toFixed(2)}
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}