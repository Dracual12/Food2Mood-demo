'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Heart, 
  Star, 
  Clock, 
  Flame,
  ArrowRight,
  RefreshCw,
  ThumbsUp,
  ThumbsDown,
  Share2
} from 'lucide-react';
import Link from 'next/link';
import { apiService, QuestionnaireData } from '../../lib/api';

interface Recommendation {
  id: number;
  name: string;
  category: string;
  description?: string;
  price: number;
  match_score: number;
  reasons: string[];
  icon?: string;
}

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedRecommendation, setSelectedRecommendation] = useState<Recommendation | null>(null);

  useEffect(() => {
    // Загрузка рекомендаций из API
    const loadRecommendations = async () => {
      setIsLoading(true);
      
      try {
        // Получаем данные анкеты из localStorage или используем дефолтные
        const questionnaireData: QuestionnaireData = {
          mood: "Радость",
          hungry: 5,
          prefers: "Вок",
          sex: "Мужской",
          age: "25-35",
          food_style: "Обычный",
          ccal: "2000-2500",
          dont_like_to_eat: "грибы",
          like_to_eat: "мясо, рыба"
        };
        
        const apiRecommendations = await apiService.getRecommendations(questionnaireData);
        setRecommendations(apiRecommendations);
      } catch (error) {
        console.error('Error loading recommendations:', error);
        // Fallback к моковым данным
        const mockRecommendations: Recommendation[] = [
        {
          id: 1,
          name: "Вок гречневый с креветками в устричном соусе",
          category: "Вок",
          description: "Богатое белком блюдо с тигровыми креветками и гречневой лапшой. Идеально подходит для поднятия настроения и восстановления энергии.",
          price: 527,
          rating: 4.8,
          match_score: 95,
          reasons: [
            "Высокое содержание белка поднимет настроение",
            "Гречневая лапша даст энергию на весь день",
            "Устричный соус добавит пикантности"
          ]
        },
        {
          id: 2,
          name: "Вок с беконом и грибами в сливочном соусе",
          category: "Вок",
          description: "Сытное блюдо с беконом и грибами в нежном сливочном соусе. Отлично подходит для комфортного ужина.",
          price: 477,
          rating: 4.6,
          match_score: 88,
          reasons: [
            "Бекон поднимет настроение",
            "Сливочный соус создаст ощущение комфорта",
            "Грибы добавят глубины вкуса"
          ]
        },
        {
          id: 3,
          name: "Корейский стритфуд с курицей",
          category: "Корейский стритфуд",
          description: "Острое и пикантное блюдо с курицей в корейском стиле. Идеально для тех, кто любит яркие вкусы.",
          price: 350,
          rating: 4.7,
          match_score: 82,
          reasons: [
            "Острота поможет справиться со стрессом",
            "Курица - отличный источник белка",
            "Корейские специи поднимут настроение"
          ]
        }
      ];
      
        setRecommendations(mockRecommendations);
      }
      
      setIsLoading(false);
    };

    loadRecommendations();
  }, []);

  const handleFeedback = (recommendationId: number, isPositive: boolean) => {
    // Здесь будет отправка отзыва на API
    console.log(`Отзыв для блюда ${recommendationId}: ${isPositive ? 'положительный' : 'отрицательный'}`);
  };

  const handleShare = (recommendation: Recommendation) => {
    // Здесь будет функционал шаринга
    console.log('Поделиться рекомендацией:', recommendation.name);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-dots mx-auto mb-8">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Анализируем твои предпочтения...
          </h2>
          <p className="text-gray-600">
            Наша AI-система подбирает идеальные блюда специально для тебя
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-gradient">Food2Mood</span>
          </div>
          
          <Link href="/" className="text-gray-600 hover:text-primary-600 transition-colors">
            На главную
          </Link>
        </div>
      </header>

      {/* Content */}
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Твои персональные рекомендации ✨
          </h1>
          <p className="text-xl text-gray-600">
            AI подобрал идеальные блюда под твое настроение и предпочтения
          </p>
        </motion.div>

        {/* Recommendations Grid */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {recommendations.map((recommendation, index) => (
            <motion.div
              key={recommendation.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="recommendation-card"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-sm font-medium text-primary-600 bg-primary-100 px-3 py-1 rounded-full">
                      {recommendation.category}
                    </span>
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4 text-yellow-500 fill-current" />
                      <span className="text-sm font-medium text-gray-600">
                        {recommendation.rating}
                      </span>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {recommendation.name}
                  </h3>
                  
                  <p className="text-gray-600 mb-4">
                    {recommendation.description}
                  </p>
                </div>
                
                <div className="text-right">
                  <div className="text-2xl font-bold text-primary-600">
                    {recommendation.price}₽
                  </div>
                  <div className="text-sm text-gray-500">
                    за порцию
                  </div>
                </div>
              </div>

              {/* Match Score */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    Совпадение с твоими предпочтениями
                  </span>
                  <span className="text-sm font-bold text-primary-600">
                    {recommendation.match_score}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div 
                    className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${recommendation.match_score}%` }}
                    transition={{ duration: 1, delay: index * 0.2 }}
                  />
                </div>
              </div>

              {/* Reasons */}
              <div className="mb-6">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  Почему именно это блюдо:
                </h4>
                <ul className="space-y-1">
                  {recommendation.reasons.map((reason, reasonIndex) => (
                    <li key={reasonIndex} className="text-sm text-gray-600 flex items-start">
                      <span className="text-primary-500 mr-2">•</span>
                      {reason}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleFeedback(recommendation.id, true)}
                    className="flex items-center space-x-1 px-3 py-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                  >
                    <ThumbsUp className="w-4 h-4" />
                    <span className="text-sm">Нравится</span>
                  </button>
                  
                  <button
                    onClick={() => handleFeedback(recommendation.id, false)}
                    className="flex items-center space-x-1 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <ThumbsDown className="w-4 h-4" />
                    <span className="text-sm">Не нравится</span>
                  </button>
                </div>
                
                <button
                  onClick={() => handleShare(recommendation)}
                  className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <Share2 className="w-4 h-4" />
                  <span className="text-sm">Поделиться</span>
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* AI Analysis */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card p-8 mb-8"
        >
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center flex-shrink-0">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Анализ AI-системы
              </h3>
              <p className="text-gray-600 mb-4">
                Основываясь на твоем настроении и предпочтениях, мы подобрали блюда, которые:
              </p>
              <ul className="space-y-2">
                <li className="flex items-start">
                  <span className="text-primary-500 mr-2">🧠</span>
                  <span className="text-gray-600">Помогут поднять настроение благодаря правильному балансу питательных веществ</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-500 mr-2">❤️</span>
                  <span className="text-gray-600">Соответствуют твоим вкусовым предпочтениям и диетическим ограничениям</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-500 mr-2">⚡</span>
                  <span className="text-gray-600">Дадут энергию на весь день благодаря оптимальному содержанию калорий</span>
                </li>
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="btn-primary flex items-center space-x-2">
            <RefreshCw className="w-5 h-5" />
            <span>Получить новые рекомендации</span>
          </button>
          
          <Link href="/questionnaire" className="btn-secondary flex items-center space-x-2">
            <span>Изменить предпочтения</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
