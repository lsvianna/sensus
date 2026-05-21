import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setToken: (token) => set({ token }),
  logout: () => set({ user: null, token: null, isAuthenticated: false }),
}));

export const useAccountStore = create((set) => ({
  accounts: [],
  selectedAccount: null,
  loading: false,
  error: null,
  
  setAccounts: (accounts) => set({ accounts }),
  setSelectedAccount: (account) => set({ selectedAccount: account }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));

export const usePostsStore = create((set) => ({
  posts: [],
  loading: false,
  error: null,
  
  setPosts: (posts) => set({ posts }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
