"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { publicApi } from "@/lib/api";
import type { MenuItem, Tag } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import MenuCard from "@/components/MenuCard";

export default function MenuPage() {
  const router = useRouter();
  const [tags, setTags] = useState<Tag[]>([]);
  const [items, setItems] = useState<MenuItem[]>([]);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    publicApi.listTags().then(setTags).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    publicApi
      .listMenu({ tag_id: selectedTag ?? undefined, search: search || undefined })
      .then(setItems)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedTag, search]);

  function handleSearch(v: string) {
    setSearch(v);
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => {}, 0);
  }

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-border bg-background/95 px-4 py-3 backdrop-blur">
        <div className="flex items-center gap-2">
          <button
            onClick={() => router.back()}
            className="shrink-0 text-muted-foreground hover:text-foreground"
          >
            ←
          </button>
          <Input
            placeholder="이름이나 설명으로 검색..."
            value={search}
            onChange={(e) => handleSearch(e.target.value)}
            className="h-9 flex-1 bg-card border-border"
          />
        </div>

        {/* Tag filter — horizontal scroll */}
        {tags.length > 0 && (
          <div className="no-scrollbar mt-2 flex gap-2 overflow-x-auto pb-1">
            <button
              onClick={() => setSelectedTag(null)}
              className="shrink-0"
            >
              <Badge
                variant={selectedTag === null ? "default" : "outline"}
                className="cursor-pointer whitespace-nowrap"
              >
                전체
              </Badge>
            </button>
            {tags.map((tag) => (
              <button
                key={tag.id}
                onClick={() => setSelectedTag(selectedTag === tag.id ? null : tag.id)}
                className="shrink-0"
              >
                <Badge
                  variant={selectedTag === tag.id ? "default" : "outline"}
                  className="cursor-pointer whitespace-nowrap"
                >
                  {tag.display_name}
                </Badge>
              </button>
            ))}
          </div>
        )}
      </header>

      {/* Item grid */}
      <main className="flex-1 px-4 py-4">
        {loading ? (
          <div className="flex justify-center py-16 text-muted-foreground">불러오는 중...</div>
        ) : items.length === 0 ? (
          <div className="flex justify-center py-16 text-muted-foreground">해당하는 메뉴가 없어요</div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {items.map((item) => (
              <MenuCard
                key={item.id}
                item={item}
                onClick={() => router.push(`/menu/${item.id}`)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
