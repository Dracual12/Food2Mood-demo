import type { Metadata } from 'next';
import { Inter, Poppins } from 'next/font/google';
import './globals.css';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-poppins',
});

export const metadata: Metadata = {
  title: 'Food2Mood - AI-система персональных рекомендаций еды',
  description: 'Получай персональные рекомендации блюд под свое настроение с помощью AI-технологий. Food2Mood анализирует твое состояние и подбирает идеальные блюда.',
  keywords: 'еда, рекомендации, AI, настроение, персональные рекомендации, ресторан, меню',
  authors: [{ name: 'Food2Mood Team' }],
  openGraph: {
    title: 'Food2Mood - AI-система персональных рекомендаций еды',
    description: 'Получай персональные рекомендации блюд под свое настроение с помощью AI-технологий.',
    type: 'website',
    locale: 'ru_RU',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Food2Mood - AI-система персональных рекомендаций еды',
    description: 'Получай персональные рекомендации блюд под свое настроение с помощью AI-технологий.',
  },
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru" className={`${inter.variable} ${poppins.variable}`}>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="theme-color" content="#ef4444" />
      </head>
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  );
}
