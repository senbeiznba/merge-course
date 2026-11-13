import Link from "next/link";

export default function AboutPage() {
  return (
    <main className="max-w-3xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">О проекте</h1>
      <p className="text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">
        Данный каталог курсов разработан в рамках лабораторной работы №1.
      </p>
      <Link href="/courses" className="text-blue-600 hover:underline">
        ← Назад к списку курсов
      </Link>
    </main>
  );
}