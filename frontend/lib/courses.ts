const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Course {
  id: number;
  title: string;
  description: string;
  price?: number;
}

export async function getCourses(): Promise<Course[]> {
  try {
    const res = await fetch(`${API_URL}/courses`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch courses");
    return res.json();
  } catch (error) {
    console.error("Error fetching courses:", error);
    return [];
  }
}

export async function getCourse(id: string): Promise<Course | null> {
  try {
    const res = await fetch(`${API_URL}/courses/${id}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    console.error(`Error fetching course ${id}:`, error);
    return null;
  }
}