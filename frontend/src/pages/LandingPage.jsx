import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
`;

const Hero = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 48px;
  margin-bottom: 20px;
`;

const Subtitle = styled.p`
  font-size: 18px;
  margin-bottom: 30px;
  opacity: 0.9;
`;

const Features = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 50px;
`;

const FeatureCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const FeatureTitle = styled.h3`
  margin-top: 0;
`;

function LandingPage() {
  return (
    <Container>
      <Hero>
        <Title>🎬 InstaBrush</Title>
        <Subtitle>Monitore e analise o engajamento do Instagram em tempo real</Subtitle>

        <Features>
          <FeatureCard>
            <FeatureTitle>📊 Analytics em Tempo Real</FeatureTitle>
            <p>Veja dados atualizados sobre seus posts e comentários</p>
          </FeatureCard>

          <FeatureCard>
            <FeatureTitle>💭 Análise de Sentimento</FeatureTitle>
            <p>Entenda o sentimento dos seus seguidores</p>
          </FeatureCard>

          <FeatureCard>
            <FeatureTitle>📈 Tendências</FeatureTitle>
            <p>Identifique padrões e otimize seu conteúdo</p>
          </FeatureCard>

          <FeatureCard>
            <FeatureTitle>🎯 Segmentação</FeatureTitle>
            <p>Monitore múltiplas contas de uma vez</p>
          </FeatureCard>

          <FeatureCard>
            <FeatureTitle>🔐 Privado e Seguro</FeatureTitle>
            <p>Seus dados são 100% privados</p>
          </FeatureCard>

          <FeatureCard>
            <FeatureTitle>⚡ Rápido</FeatureTitle>
            <p>Performance otimizada para todos os dispositivos</p>
          </FeatureCard>
        </Features>
      </Hero>
    </Container>
  );
}

export default LandingPage;
