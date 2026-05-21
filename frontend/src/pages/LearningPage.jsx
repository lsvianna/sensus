import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
`;

function LearningPage() {
  return (
    <Container>
      <h2>🔬 Experiência de Aprendizado</h2>
      <p>Este espaço orienta como experimentar com o pipeline de análise e ML.</p>
      <ul>
        <li>Use o endpoint <code>/api/posts/:id/analyze</code> para disparar análise.</li>
        <li>Crie experimentos com <code>POST /api/ml/train</code>.</li>
        <li>Veja o guia em <code>notebooks/learning_experience.md</code>.</li>
      </ul>
    </Container>
  );
}

export default LearningPage;
