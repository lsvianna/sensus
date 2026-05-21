import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { postsAPI } from '../api';

const Container = styled.div`
  padding: 20px;
`;

const PostList = styled.div`
  display: grid;
  gap: 15px;
`;

const PostCard = styled.div`
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const PostHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
`;

const PostDate = styled.span`
  font-size: 12px;
  color: #999;
`;

const Caption = styled.p`
  color: #333;
  margin: 10px 0;
  line-height: 1.5;
`;

const Metrics = styled.div`
  display: flex;
  gap: 20px;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
`;

const Metric = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
`;

const SentimentBadge = styled.span`
  padding: 4px 8px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: bold;
  background: ${props => {
    if (props.sentiment === 'positive') return '#d4edda';
    if (props.sentiment === 'negative') return '#f8d7da';
    return '#e2e3e5';
  }};
  color: ${props => {
    if (props.sentiment === 'positive') return '#155724';
    if (props.sentiment === 'negative') return '#721c24';
    return '#383d41';
  }};
`;

function PostsList({ accountId }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await postsAPI.list(accountId, 20);
        setPosts(response.data.posts);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };

    if (accountId) {
      fetchPosts();
    }
  }, [accountId]);

  if (loading) return <Container>Carregando posts...</Container>;

  return (
    <Container>
      <h3>📱 Posts Recentes</h3>
      {posts.length === 0 ? (
        <p>Nenhum post encontrado</p>
      ) : (
        <PostList>
          {posts.map(post => (
            <PostCard key={post.id}>
              <PostHeader>
                <PostDate>{new Date(post.posted_at).toLocaleDateString('pt-BR')}</PostDate>
                <SentimentBadge sentiment={post.sentiment_label}>
                  {post.sentiment_label}
                </SentimentBadge>
              </PostHeader>
              
              <Caption>{post.caption?.substring(0, 150)}...</Caption>
              
              <Metrics>
                <Metric>❤️ {post.likes_count} likes</Metric>
                <Metric>💬 {post.comments_count} comentários</Metric>
                <Metric>📊 {post.engagement_rate.toFixed(2)}% engajamento</Metric>
              </Metrics>
            </PostCard>
          ))}
        </PostList>
      )}
    </Container>
  );
}

export default PostsList;
