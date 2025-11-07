import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Types
export interface User {
  user_id: number;
  user_name?: string;
  user_first_name?: string;
  user_last_name?: string;
  user_link: string;
  phone?: string;
  user_reg_time: string;
  ban: boolean;
  foodToMoodCoin: number;
}

export interface MenuItem {
  id: number;
  dish_name: string;
  dish_category?: string;
  dish_price: number;
  dish_g?: string;
  size?: string;
  simple_ingridients?: string;
  additional_dishes?: string;
  iiko_id?: string;
  dish_rec_nutritionist?: string;
  dish_rec_community?: string;
  dish_rec_a_oblomov?: string;
  dish_rec_a_ivlev?: string;
  stat_reviews?: string;
  stat_rating?: string;
}

export interface QuestionnaireData {
  mood: string;
  hungry: number;
  prefers: string;
  sex: string;
  age: string;
  food_style: string;
  ccal: string;
  dont_like_to_eat: string;
  like_to_eat: string;
}

export interface Recommendation {
  id: number;
  dish_name: string;
  dish_category: string;
  dish_price: number;
  match_score: number;
  reasons: string[];
  description: string;
}

// API Methods
export const apiService = {
  // User methods
  async registerUser(userData: Partial<User>) {
    const response = await api.post('/api/v1/users/register', userData);
    return response.data;
  },

  async loginUser(userId: number) {
    const response = await api.post('/api/v1/users/login', { user_id: userId });
    return response.data;
  },

  async getUserInfo() {
    const response = await api.get('/api/v1/users/me');
    return response.data;
  },

  // Menu methods
  async getMenuItems(filters?: {
    category?: string;
    restaurant?: string;
    min_price?: number;
    max_price?: number;
  }) {
    const response = await api.get('/api/v1/menu/', { params: filters });
    return response.data;
  },

  async getCategories() {
    const response = await api.get('/api/v1/menu/categories');
    return response.data;
  },

  async getRestaurants() {
    const response = await api.get('/api/v1/menu/restaurants');
    return response.data;
  },

  async searchMenu(query: string, filters?: {
    category?: string;
    restaurant?: string;
    min_price?: number;
    max_price?: number;
  }) {
    const response = await api.get('/api/v1/menu/search', { 
      params: { query, ...filters } 
    });
    return response.data;
  },

  async getDishById(dishId: number) {
    const response = await api.get(`/api/v1/menu/${dishId}`);
    return response.data;
  },

  // Recommendations
  async getRecommendations(questionnaireData: QuestionnaireData) {
    try {
      const response = await api.post('/api/v1/recommendations', {
        user_id: 1, // Временный ID пользователя
        mood: questionnaireData.mood,
        style: questionnaireData.food_style,
        like_to_eat: questionnaireData.like_to_eat,
        dont_like_to_eat: questionnaireData.dont_like_to_eat,
        category: questionnaireData.prefers
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Fallback to mock data if API fails
      return [];
    }
  },

  // Orders
  async createOrder(orderData: {
    user_id: number;
    table_number?: number;
    order_amount: number;
    basket: any;
  }) {
    const response = await api.post('/api/v1/orders/', orderData);
    return response.data;
  },

  async getUserOrders(userId?: number) {
    const response = await api.get('/api/v1/orders/', { 
      params: { user_id: userId } 
    });
    return response.data;
  },

  async getOrderStats() {
    const response = await api.get('/api/v1/orders/stats/overview');
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;
