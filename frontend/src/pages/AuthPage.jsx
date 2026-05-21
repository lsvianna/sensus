import React, { useState } from 'react';
import styled from 'styled-components';
import { useAuthStore } from '../store';

const Container = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const Card = styled.div`
  background: white;
  border-radius: 10px;
  padding: 40px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
`;

const Title = styled.h1`
  text-align: center;
  color: #333;
  margin-bottom: 30px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const Input = styled.input`
  padding: 12px;
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
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  
  &:hover {
    background: #5568d3;
  }
`;

const Toggle = styled.div`
  text-align: center;
  font-size: 14px;
  color: #666;
  
  button {
    background: none;
    border: none;
    color: #667eea;
    cursor: pointer;
    font-weight: bold;
    
    &:hover {
      text-decoration: underline;
    }
  }
`;

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const setUser = useAuthStore(state => state.setUser);

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement auth with backend
    console.log(isLogin ? 'Login' : 'Signup', { email, password, username });
    setUser({ email, username });
  };

  return (
    <Container>
      <Card>
        <Title>🎬 InstaBrush</Title>
        
        <Form onSubmit={handleSubmit}>
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          
          {!isLogin && (
            <Input
              type="text"
              placeholder="Nome de usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          )}
          
          <Input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <Button type="submit">
            {isLogin ? 'Entrar' : 'Criar Conta'}
          </Button>
        </Form>

        <Toggle>
          {isLogin ? 'Novo por aqui?' : 'Já tem conta?'}
          <br />
          <button type="button" onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? 'Criar conta' : 'Entrar'}
          </button>
        </Toggle>
      </Card>
    </Container>
  );
}

export default AuthPage;
