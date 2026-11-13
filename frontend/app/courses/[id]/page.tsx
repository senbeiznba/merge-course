import { getCourse, getCourses } from "@/lib/courses";
import { notFound } from "next/navigation";
import LikeButton from "@/components/LikeButton";

export async function generateStaticParams() {
  const courses = await getCourses();
  return courses.map((course) => ({
    id: course.id,
  }));
}

type CoursePageProps = {
  params: Promise<{ id: string }>;
};

export default async function CoursePage({ params }: CoursePageProps) {
  const { id } = await params;
  const course = await getCourse(id);

  if (!course) {
    notFound();
  }

  return (
    <main className="max-w-3xl mx-auto p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">{course.title}</h1>
        <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2.5 py-0.5 rounded font-semibold">
          {course.isElective ? "Элективный курс" : "Обязательный курс"}
        </span>
      </div>

      <p className="text-lg text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
        {course.description}
      </p>

      <div className="flex justify-between items-center border-t pt-6 border-gray-200 dark:border-zinc-800">
        <span className="text-gray-600 dark:text-gray-400 font-medium">
          Кредиты: {course.credits}
        </span>
        <LikeButton initialLikes={course.likes} />
      </div>
    </main>
  );
}