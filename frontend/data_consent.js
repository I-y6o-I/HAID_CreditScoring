import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendConsent } from '../api';
import './Consent.css';

export default function Consent() {
  const [consent, setConsent] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    await sendConsent({ consent });
    navigate('/application');
  };

  return (
    <div className="consent-container">
      <h2>Использование данных</h2>
      <p>Мы используем ваши данные только для расчета скоринга</p>
      
      <div className="consent-options">
        <label>
          <input
            type="radio"
            checked={consent === true}
            onChange={() => setConsent(true)}
          />
          Разрешаю хранение данных
        </label>
        
        <label>
          <input
            type="radio"
            checked={consent === false}
            onChange={() => setConsent(false)}
          />
          Не разрешаю
        </label>
      </div>

      <button
        disabled={consent === null}
        onClick={handleSubmit}
      >
        Продолжить
      </button>
    </div>
  );
}