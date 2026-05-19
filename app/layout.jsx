import './globals.css';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/ThemeProvider';

const inter = Inter({ subsets: ['latin'] });

import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export const metadata = {
  title: 'Amarnath MB | Full Stack Developer & Data Analyst',
  description: 'Portfolio website of Amarnath MB, a final year student passionate about Full Stack Development, Data Analytics, and AI.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen flex flex-col bg-background text-foreground`}>
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
          <Navbar />
          {children}
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
