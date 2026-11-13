import Link from "next/link";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className="bg-zinc-50 dark:bg-black text-black dark:text-zinc-50 min-h-screen">
        <nav className="flex gap-6 p-4 border-b border-gray-200 dark:border-zinc-800 max-w-5xl mx-auto">
          <Link href="/" className="hover:text-blue-600 font-medium">Главная</Link>
          <Link href="/courses" className="hover:text-blue-600 font-medium">Курсы</Link>
          <Link href="/about" className="hover:text-blue-600 font-medium">О нас</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}