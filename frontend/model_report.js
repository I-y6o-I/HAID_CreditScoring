import { useEffect, useState } from 'react';
import { getModelReport } from '../api';
import './ModelReport.css';

export default function ModelReport() {
  const [report, setReport] = useState(null);

  useEffect(() => {
    getModelReport().then(setReport);
  }, []);

  return (
    <div className="report-container">
      <h2>Технический отчет модели</h2>
      
      {report && (
        <>
          <div className="metrics">
            <h3>Метрики:</h3>
            <p>Accuracy: {report.accuracy}</p>
            <p>Precision: {report.precision}</p>
            <p>Recall: {report.recall}</p>
          </div>

          <div className="bias-audit">
            <h3>Проверка на смещения:</h3>
            <ul>
              {report.bias_checks.map((check, i) => (
                <li key={i}>{check}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}