"use client";

import { useState } from "react";

type LikeButtonProps = {
  initialLikes: number;
};

export default function LikeButton({ initialLikes }: LikeButtonProps) {
  const [likes, setLikes] = useState<number>(initialLikes);

  return (
    <button
      onClick={() => setLikes((prev) => prev + 1)}
      className="flex items-center gap-2 px-4 py-2 border rounded-full hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors font-medium"
    >
      <span>❤️</span>
      <span>{likes}</span>
    </button>
  );
}