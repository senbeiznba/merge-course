import Link from "next/link";

type CourseCardProps = {
  id: string;
  title: string;
  description: string;
  credits: number;
  likes: number;
};

export default function CourseCard({ id, title, description, credits, likes }: CourseCardProps) {
  return (
    <Link 
      href={`/courses/${id}`}
      className="block p-6 border rounded-xl hover:shadow-lg transition-shadow bg-white dark:bg-zinc-900 border-gray-200 dark:border-zinc-800"
    >
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">{description}</p>
      <div className="flex justify-between items-center text-sm font-medium text-gray-500 dark:text-gray-400">
        <span>Кредитов: {credits}</span>
        <span>❤️ {likes}</span>
      </div>
    </Link>
  );
}