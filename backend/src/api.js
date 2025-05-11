const API_URL = 'http://localhost:8000/api/v1';

export const sendConsent = (data) => {
  return fetch(`${API_URL}/consent`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
};

export const submitApplication = (data) => {
  return fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json());
};