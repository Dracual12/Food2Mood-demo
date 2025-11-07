'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Heart, 
  Brain, 
  Utensils, 
  ArrowRight, 
  ArrowLeft,
  Check,
  Smile,
  Frown,
  Meh,
  Star
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface QuestionnaireData {
  // Первая анкета (настроение и голод)
  mood: string;
  hungry: number;
  prefers: string;
  
  // Вторая анкета (предпочтения)
  sex: string;
  age: string;
  food_style: string;
  ccal: string;
  dont_like_to_eat: string;
  like_to_eat: string;
}

export default function QuestionnairePage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState<QuestionnaireData>({
    mood: '',
    hungry: 5,
    prefers: '',
    sex: '',
    age: '',
    food_style: '',
    ccal: '',
    dont_like_to_eat: '',
    like_to_eat: ''
  });

  const moods = [
    { id: 'Спокойствие', label: 'Спокойствие', emoji: '😌', color: 'from-blue-500 to-blue-600' },
    { id: 'Радость', label: 'Радость', emoji: '😊', color: 'from-yellow-500 to-yellow-600' },
    { id: 'Печаль', label: 'Печаль', emoji: '😢', color: 'from-gray-500 to-gray-600' },
    { id: 'Гнев', label: 'Гнев', emoji: '😠', color: 'from-red-500 to-red-600' },
    { id: 'Волнение', label: 'Волнение', emoji: '🤩', color: 'from-purple-500 to-purple-600' }
  ];

  const foodStyles = [
    { id: 'Стандартное', label: 'Стандартное питание', emoji: '🍽️' },
    { id: 'Вегетарианское', label: 'Вегетарианское', emoji: '🥗' },
    { id: 'Веганское', label: 'Веганское', emoji: '🌱' },
    { id: 'Кето', label: 'Кето-диета', emoji: '🥑' },
    { id: 'Палео', label: 'Палео-диета', emoji: '🥩' }
  ];

  const ages = [
    { id: 'До 18', label: 'До 18 лет', emoji: '👶' },
    { id: '18-25', label: '18-25 лет', emoji: '🧑' },
    { id: '26-35', label: '26-35 лет', emoji: '👨‍🦱' },
    { id: '36-45', label: '36-45 лет', emoji: '🧔‍️' },
    { id: '45+', label: '45+ лет', emoji: '👴' }
  ];

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
    }
  };

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    
    try {
      // Здесь будет отправка данных на API
      console.log('Отправляем данные:', data);
      
      // Имитация загрузки
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Перенаправляем на страницу результатов
      router.push('/recommendations');
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateData = (field: keyof QuestionnaireData, value: any) => {
    setData(prev => ({ ...prev, [field]: value }));
  };

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
          
          <div className="text-sm text-gray-600">
            Шаг {currentStep} из 3
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="container mx-auto px-4 mb-8">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div 
            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(currentStep / 3) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {/* Step 1: Mood and Hunger */}
          {currentStep === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Как ты себя чувствуешь? 🤔
                </h1>
                <p className="text-xl text-gray-600">
                  Расскажи о своем настроении и уровне голода
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                {/* Mood Selection */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                    <Heart className="w-6 h-6 text-primary-500 mr-2" />
                    Твое настроение
                  </h2>
                  <div className="grid grid-cols-1 gap-4">
                    {moods.map((mood) => (
                      <button
                        key={mood.id}
                        onClick={() => updateData('mood', mood.id)}
                        className={`mood-card ${data.mood === mood.id ? 'selected' : ''}`}
                      >
                        <div className="flex items-center space-x-4">
                          <span className="text-3xl">{mood.emoji}</span>
                          <span className="text-lg font-medium">{mood.label}</span>
                          {data.mood === mood.id && (
                            <Check className="w-6 h-6 text-primary-500 ml-auto" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Hunger Level */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                    <Utensils className="w-6 h-6 text-primary-500 mr-2" />
                    Уровень голода
                  </h2>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-primary-600 mb-4">
                      {data.hungry}/10
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={data.hungry}
                      onChange={(e) => updateData('hungry', parseInt(e.target.value))}
                      className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                    />
                    <div className="flex justify-between text-sm text-gray-500 mt-2">
                      <span>Не голоден</span>
                      <span>Очень голоден</span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 2: Preferences */}
          {currentStep === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Расскажи о своих предпочтениях 👤
                </h1>
                <p className="text-xl text-gray-600">
                  Это поможет нам лучше понять твои вкусы
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                {/* Sex */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                    Пол
                  </h2>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { id: 'Мужской', label: 'Мужской', emoji: '👨' },
                      { id: 'Женский', label: 'Женский', emoji: '👩' }
                    ].map((option) => (
                      <button
                        key={option.id}
                        onClick={() => updateData('sex', option.id)}
                        className={`mood-card ${data.sex === option.id ? 'selected' : ''}`}
                      >
                        <div className="text-center">
                          <div className="text-3xl mb-2">{option.emoji}</div>
                          <div className="font-medium">{option.label}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Age */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                    Возраст
                  </h2>
                  <div className="grid grid-cols-1 gap-3">
                    {ages.map((age) => (
                      <button
                        key={age.id}
                        onClick={() => updateData('age', age.id)}
                        className={`mood-card ${data.age === age.id ? 'selected' : ''}`}
                      >
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{age.emoji}</span>
                          <span className="font-medium">{age.label}</span>
                          {data.age === age.id && (
                            <Check className="w-5 h-5 text-primary-500 ml-auto" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Food Style */}
                <div className="card p-8 md:col-span-2">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                    Стиль питания
                  </h2>
                  <div className="grid md:grid-cols-3 gap-4">
                    {foodStyles.map((style) => (
                      <button
                        key={style.id}
                        onClick={() => updateData('food_style', style.id)}
                        className={`mood-card ${data.food_style === style.id ? 'selected' : ''}`}
                      >
                        <div className="text-center">
                          <div className="text-3xl mb-2">{style.emoji}</div>
                          <div className="font-medium">{style.label}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 3: Food Preferences */}
          {currentStep === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Твои вкусовые предпочтения 🍽️
                </h1>
                <p className="text-xl text-gray-600">
                  Что ты любишь и что не ешь?
                </p>
              </div>

              <div className="space-y-8">
                {/* Don't like */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                    <Frown className="w-6 h-6 text-red-500 mr-2" />
                    Что ты НЕ ешь? 💔
                  </h2>
                  <textarea
                    value={data.dont_like_to_eat}
                    onChange={(e) => updateData('dont_like_to_eat', e.target.value)}
                    placeholder="Например: грибы, морепродукты, острое..."
                    className="input-field h-24 resize-none"
                  />
                </div>

                {/* Like */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                    <Smile className="w-6 h-6 text-green-500 mr-2" />
                    Что ты ЛЮБИШЬ? ❤️
                  </h2>
                  <textarea
                    value={data.like_to_eat}
                    onChange={(e) => updateData('like_to_eat', e.target.value)}
                    placeholder="Например: паста, суши, десерты..."
                    className="input-field h-24 resize-none"
                  />
                </div>

                {/* Calories */}
                <div className="card p-8">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                    Калории на блюдо (опционально)
                  </h2>
                  <input
                    type="text"
                    value={data.ccal}
                    onChange={(e) => updateData('ccal', e.target.value)}
                    placeholder="Например: 300-500 ккал"
                    className="input-field"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex justify-between items-center mt-12 max-w-4xl mx-auto">
          <button
            onClick={handlePrev}
            disabled={currentStep === 1}
            className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Назад</span>
          </button>

          <button
            onClick={handleNext}
            disabled={isLoading}
            className="btn-primary flex items-center space-x-2"
          >
            {isLoading ? (
              <div className="loading-dots">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
              </div>
            ) : currentStep === 3 ? (
              <>
                <span>Получить рекомендации</span>
                <Star className="w-5 h-5" />
              </>
            ) : (
              <>
                <span>Далее</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
