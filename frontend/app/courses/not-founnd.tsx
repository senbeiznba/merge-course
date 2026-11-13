import Link from "next/link";

export default function NotFound() {
  return (
    <main className="max-w-md mx-auto p-8 text-center">
      <h1 className="text-2xl font-bold mb-4">Курс не найден</h1>
      <p className="text-gray-600 mb-6">Запрошенный курс не существует.</p>
      <Link href="/courses" className="text-blue-600 hover:underline">
        Вернуться к списку курсов
      </Link>
    </main>
  );
}