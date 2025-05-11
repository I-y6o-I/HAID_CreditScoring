import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitApplication } from '../api';
import './ApplicationForm.css';

const fieldLabels = {
  code_gender: 'Пол',
  days_birth: 'Возраст',
  amt_income_total: 'Доход',
  // ... остальные поля
};

export default function ApplicationForm() {
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await submitApplication(formData);
    navigate('/results', { state: response });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Кредитная заявка</h2>
      
      <div className="form-section">
        <label>{fieldLabels.code_gender}</label>
        <select
          value={formData.code_gender}
          onChange={(e) => setFormData({...formData, code_gender: e.target.value})}
        >
          <option value="M">Мужской</option>
          <option value="F">Женский</option>
        </select>
      </div>

      {/* Другие поля формы */}

      <button type="submit">Отправить</button>
    </form>
  );
}