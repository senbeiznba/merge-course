import Link from "next/link";
import { getCourses } from "@/lib/courses";

export default async function Home() {
  const courses = await getCourses();

  return (
    <main className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] p-8 text-center">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Каталог Курсов IT
      </h1>
      <p className="text-lg text-gray-600 dark:text-gray-400 max-w-xl mb-8">
        Добро пожаловать в учебный каталог курсов! Здесь собраны актуальные дисциплины по фронтенду, бэкенду, базам данных и безопасности.
      </p>

      <div className="flex gap-4">
        <Link
          href="/courses"
          className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Перейти к курсам ({courses.length})
        </Link>
        <Link
          href="/about"
          className="px-6 py-3 border border-gray-300 dark:border-gray-700 font-medium rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          О проекте
        </Link>
      </div>
    </main>
  );
}