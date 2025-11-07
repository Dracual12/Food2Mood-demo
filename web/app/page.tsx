'use client';

import { useState } from 'react';
import { 
  Brain, 
  Heart, 
  Utensils, 
  Star, 
  ArrowRight, 
  Sparkles,
  Users,
  TrendingUp,
  Shield
} from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleGetStarted = () => {
    setIsLoading(true);
    // Redirect to questionnaire
    setTimeout(() => {
      window.location.href = '/questionnaire';
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-gradient">Food2Mood</span>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link href="#features" className="text-gray-600 hover:text-primary-600 transition-colors">
              Возможности
            </Link>
            <Link href="#how-it-works" className="text-gray-600 hover:text-primary-600 transition-colors">
              Как это работает
            </Link>
            <Link href="#about" className="text-gray-600 hover:text-primary-600 transition-colors">
              О нас
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <div>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
            Персональные рекомендации еды
            <span className="text-gradient block mt-2">под твое настроение</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            AI-помощник <strong>Food2Mood</strong> анализирует твое состояние, 
            вкусовые предпочтения и подбирает идеальные блюда для каждого момента жизни
          </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button 
              onClick={handleGetStarted}
              disabled={isLoading}
              className="btn-primary text-lg px-8 py-4 flex items-center space-x-2 group"
            >
              {isLoading ? (
                <div className="loading-dots">
                  <div></div>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              ) : (
                <>
                  <span>Начать анализ</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
            
            <Link href="#how-it-works" className="btn-secondary text-lg px-8 py-4 flex items-center space-x-2">
              <span>Узнать больше</span>
              <Sparkles className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white/50">
        <div className="container mx-auto px-4">
          <div
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Почему выбирают Food2Mood?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Умная система, которая понимает тебя лучше, чем ты сам
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: "AI-анализ настроения",
                description: "Нейросеть анализирует твое эмоциональное состояние и подбирает блюда, которые поднимут настроение"
              },
              {
                icon: Heart,
                title: "Персональные предпочтения",
                description: "Учитываем твои вкусы, аллергии, диетические ограничения и предпочтения в еде"
              },
              {
                icon: TrendingUp,
                title: "Постоянное обучение",
                description: "Система становится умнее с каждым отзывом, улучшая рекомендации специально для тебя"
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="card p-8 text-center"
              >
                <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4">
          <div
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Как это работает?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Всего 3 простых шага до идеальных рекомендаций
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Расскажи о себе",
                description: "Заполни быструю анкету о своем настроении, голоде и вкусовых предпочтениях"
              },
              {
                step: "02", 
                title: "AI анализирует",
                description: "Наша нейросеть обрабатывает данные и подбирает идеальные блюда под твое состояние"
              },
              {
                step: "03",
                title: "Получай рекомендации",
                description: "Получай персональные рекомендации блюд с объяснением, почему именно они подходят тебе"
              }
            ].map((step, index) => (
              <div
                key={index}
                className="text-center"
              >
                <div className="w-20 h-20 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                  {step.step}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {step.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-primary-500 to-secondary-500">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center text-white">
            {[
              { number: "10K+", label: "Довольных пользователей" },
              { number: "95%", label: "Точность рекомендаций" },
              { number: "50K+", label: "Анализированных блюд" },
              { number: "24/7", label: "Доступность сервиса" }
            ].map((stat, index) => (
              <div
                key={index}
              >
                <div className="text-4xl font-bold mb-2">{stat.number}</div>
                <div className="text-primary-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <div
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Готов найти идеальное блюдо?
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Присоединяйся к тысячам пользователей, которые уже нашли свой идеальный вкус
            </p>
            <button 
              onClick={handleGetStarted}
              disabled={isLoading}
              className="btn-primary text-lg px-8 py-4 flex items-center space-x-2 mx-auto group"
            >
              {isLoading ? (
                <div className="loading-dots">
                  <div></div>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              ) : (
                <>
                  <span>Начать анализ</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </div>
          </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">Food2Mood</span>
              </div>
              <p className="text-gray-400">
                AI-система персональных рекомендаций еды под настроение
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Продукт</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#features">Возможности</Link></li>
                <li><Link href="#how-it-works">Как работает</Link></li>
                <li><Link href="/questionnaire">Начать анализ</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Поддержка</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#about">О нас</Link></li>
                <li><Link href="#contact">Контакты</Link></li>
                <li><Link href="#help">Помощь</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Следите за нами</h3>
              <div className="flex space-x-4">
                <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                  <span className="text-sm">📱</span>
                </div>
                <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                  <span className="text-sm">📧</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Food2Mood. Все права защищены.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
