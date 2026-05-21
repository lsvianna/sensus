import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { analyticsAPI } from '../api';

const Container = styled.div`
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Stat = styled.div`
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const Label = styled.div`
  font-size: 14px;
  opacity: 0.8;
`;

const SentimentChart = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
  align-items: flex-end;
`;

const Bar = styled.div`
  flex: 1;
  background: ${props => props.color};
  height: ${props => props.height}px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 5px;
  font-size: 12px;
`;

function DashboardAnalytics({ accountId }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await analyticsAPI.accountAnalytics(accountId);
        setAnalytics(response.data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    if (accountId) {
      fetchAnalytics();
    }
  }, [accountId]);

  if (loading) return <Container>Carregando...</Container>;
  if (!analytics) return <Container>Sem dados disponíveis</Container>;

  const total = Object.values(analytics.sentiment_breakdown).reduce((a, b) => a + b, 0);
  const positive = analytics.sentiment_breakdown.positive || 0;
  const negative = analytics.sentiment_breakdown.negative || 0;
  const neutral = analytics.sentiment_breakdown.neutral || 0;

  return (
    <Container>
      <h2>📊 Análise da Conta</h2>
      
      <Grid>
        <Card>
          <Stat>{analytics.total_posts}</Stat>
          <Label>Total de Posts</Label>
        </Card>
        
        <Card>
          <Stat>{analytics.average_engagement.toFixed(2)}%</Stat>
          <Label>Engajamento Médio</Label>
        </Card>
        
        <Card>
          <Stat>{analytics.total_likes}</Stat>
          <Label>Total de Likes</Label>
        </Card>
        
        <Card>
          <Stat>{analytics.total_comments}</Stat>
          <Label>Total de Comentários</Label>
        </Card>
      </Grid>

      <Card style={{ marginTop: '20px' }}>
        <Label>Sentimento dos Posts</Label>
        <SentimentChart>
          <Bar color="#10b981" height={positive * 2}>
            <span>{positive}</span>
            <small>Positivos</small>
          </Bar>
          <Bar color="#f59e0b" height={neutral * 2}>
            <span>{neutral}</span>
            <small>Neutros</small>
          </Bar>
          <Bar color="#ef4444" height={negative * 2}>
            <span>{negative}</span>
            <small>Negativos</small>
          </Bar>
        </SentimentChart>
      </Card>
    </Container>
  );
}

export default DashboardAnalytics;
