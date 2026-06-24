"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { publicApi } from "@/lib/api";
import type { MenuItem, Tag } from "@/types";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import MenuCard from "@/components/MenuCard";

type Step = "pick" | "results";

export default function WhiskyBeginnerPage() {
  const router = useRouter();
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTag, setSelectedTag] = useState<Tag | null>(null);
  const [results, setResults] = useState<MenuItem[]>([]);
  const [step, setStep] = useState<Step>("pick");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    publicApi.listTags().then(setTags).catch(() => {});
  }, []);

  async function handlePick(tag: Tag) {
    setSelectedTag(tag);
    setLoading(true);
    try {
      const data = await publicApi.listMenu({ tag_id: tag.id });
      setResults(data);
      setStep("results");
    } catch {
      /* silent */
    } finally {
      setLoading(false);
    }
  }

  if (step === "results") {
    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => setStep("pick")} className="text-muted-foreground">
            ← 다시 고르기
          </button>
          <h1 className="mt-2 text-xl font-bold">
            &quot;{selectedTag?.display_name}&quot; 스타일 추천
          </h1>
        </header>
        <main className="flex-1 px-4 py-4">
          {results.length === 0 ? (
            <p className="py-16 text-center text-muted-foreground">
              해당 스타일의 메뉴가 없어요
            </p>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {results.map((item) => (
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

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <header className="border-b border-border px-4 py-4">
        <button onClick={() => router.back()} className="text-muted-foreground">
          ← 홈으로
        </button>
        <h1 className="mt-2 text-xl font-bold">어떤 느낌의 술이 끌려요?</h1>
        <p className="text-sm text-muted-foreground">하나만 골라주세요</p>
      </header>
      <main className="flex flex-1 flex-wrap content-start gap-3 px-4 py-6">
        {loading ? (
          <p className="text-muted-foreground">불러오는 중...</p>
        ) : tags.length === 0 ? (
          <p className="text-muted-foreground">태그를 불러올 수 없어요</p>
        ) : (
          tags.map((tag) => (
            <button key={tag.id} onClick={() => handlePick(tag)} disabled={loading}>
              <Badge
                variant="outline"
                className="cursor-pointer px-4 py-2 text-base hover:border-primary hover:text-primary"
              >
                {tag.display_name}
              </Badge>
            </button>
          ))
        )}
      </main>
    </div>
  );
}
