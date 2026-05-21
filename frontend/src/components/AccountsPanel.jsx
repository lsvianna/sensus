import React, { useState } from 'react';
import styled from 'styled-components';
import { accountsAPI } from '../api';
import { useAccountStore } from '../store';

const Container = styled.div`
  padding: 20px;
`;

const Form = styled.form`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Button = styled.button`
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  
  &:hover {
    background: #5568d3;
  }
`;

const AccountsList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
`;

const AccountCard = styled.div`
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  ${props => props.selected ? 'border-color: #667eea; background: #f0f4ff;' : ''}
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const AccountName = styled.h4`
  margin: 0 0 10px 0;
  color: #333;
`;

const AccountInfo = styled.div`
  font-size: 12px;
  color: #666;
  
  div {
    margin-bottom: 5px;
  }
`;

function AccountsPanel({ userId }) {
  const [accounts, setAccounts] = useState([]);
  const [newUsername, setNewUsername] = useState('');
  const { selectedAccount, setSelectedAccount } = useAccountStore();

  React.useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const response = await accountsAPI.list(userId);
        setAccounts(response.data.accounts);
      } catch (error) {
        console.error('Error fetching accounts:', error);
      }
    };

    if (userId) {
      fetchAccounts();
    }
  }, [userId]);

  const handleAddAccount = async (e) => {
    e.preventDefault();
    try {
      await accountsAPI.create({
        user_id: userId,
        instagram_username: newUsername
      });
      setNewUsername('');
      // Refresh accounts list
      const response = await accountsAPI.list(userId);
      setAccounts(response.data.accounts);
    } catch (error) {
      alert('Erro ao adicionar conta: ' + error.message);
    }
  };

  return (
    <Container>
      <h3>📲 Suas Contas</h3>
      
      <Form onSubmit={handleAddAccount}>
        <Input
          type="text"
          placeholder="Digite o nome de usuário do Instagram..."
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <Button type="submit">+ Adicionar</Button>
      </Form>

      {accounts.length === 0 ? (
        <p>Nenhuma conta adicionada ainda</p>
      ) : (
        <AccountsList>
          {accounts.map(account => (
            <AccountCard
              key={account.id}
              selected={selectedAccount?.id === account.id}
              onClick={() => setSelectedAccount(account)}
            >
              <AccountName>@{account.username}</AccountName>
              <AccountInfo>
                <div>👥 {account.followers_count?.toLocaleString() || 'N/A'} seguidores</div>
                <div>📱 {account.posts_count} posts</div>
              </AccountInfo>
            </AccountCard>
          ))}
        </AccountsList>
      )}
    </Container>
  );
}

export default AccountsPanel;
