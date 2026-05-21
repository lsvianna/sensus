import React from 'react';
import styled from 'styled-components';
import AccountsPanel from '../components/AccountsPanel';
import DashboardAnalytics from '../components/DashboardAnalytics';
import PostsList from '../components/PostsList';
import LearningPage from './LearningPage';
import { useAccountStore } from '../store';

const Container = styled.div`
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  padding: 20px;
  background: #f9fafb;
  min-height: 100vh;
`;

const Sidebar = styled.div`
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const Header = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  
  h1 {
    margin: 0;
    color: #333;
  }
`;

function DashboardPage() {
  const { selectedAccount } = useAccountStore();
  const userId = 1; // Mock user ID
  const [showLearning, setShowLearning] = React.useState(false);

  return (
    <Container>
      <Sidebar>
        <AccountsPanel userId={userId} />
      </Sidebar>

      <MainContent>
        <Header>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <h1 style={{margin: 0}}>
                {selectedAccount
                  ? `📊 Dashboard - ${selectedAccount.username}`
                  : '👋 Bem-vindo ao InstaBrush'}
              </h1>
              <div>
                <button onClick={() => setShowLearning(s => !s)} style={{marginLeft: 12}}>
                  🔬 Aprender
                </button>
              </div>
            </div>
        </Header>

          {selectedAccount && (
          <>
            <DashboardAnalytics accountId={selectedAccount.id} />
            <PostsList accountId={selectedAccount.id} />
          </>
        )}

          {showLearning && <LearningPage />}

        {!selectedAccount && (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <p>Selecione uma conta para visualizar analytics</p>
          </div>
        )}
      </MainContent>
    </Container>
  );
}

export default DashboardPage;
