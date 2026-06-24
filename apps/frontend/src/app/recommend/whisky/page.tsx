"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { publicApi } from "@/lib/api";
import type { MenuItem } from "@/types";
import { Button } from "@/components/ui/button";
import MenuCard from "@/components/MenuCard";

type Step = "select" | "pref" | "direction" | "results";

export default function WhiskyRecommendPage() {
  const router = useRouter();
  const [allItems, setAllItems] = useState<MenuItem[]>([]);
  const [selected, setSelected] = useState<MenuItem | null>(null);
  const [liked, setLiked] = useState<boolean | null>(null);
  const [same, setSame] = useState<boolean | null>(null);
  const [results, setResults] = useState<MenuItem[]>([]);
  const [step, setStep] = useState<Step>("select");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    publicApi.listMenu().then(setAllItems).catch(() => {}).finally(() => setLoading(false));
  }, []);

  function handleSelect(item: MenuItem) {
    setSelected(item);
    setStep("pref");
  }

  function handlePref(isLiked: boolean) {
    setLiked(isLiked);
    setStep("direction");
  }

  function handleDirection(wantSame: boolean) {
    setSame(wantSame);
    if (!selected) return;

    const selectedTagIds = new Set(selected.tags.map((t) => t.tag.id));

    let candidates = allItems.filter((i) => i.id !== selected.id);

    if (wantSame) {
      // same tags → more overlap is better
      candidates = candidates
        .map((i) => ({
          item: i,
          overlap: i.tags.filter((t) => selectedTagIds.has(t.tag.id)).length,
        }))
        .filter(({ overlap }) => overlap > 0)
        .sort((a, b) => b.overlap - a.overlap)
        .map(({ item }) => item);
    } else {
      // different tags → less overlap is better
      candidates = candidates
        .map((i) => ({
          item: i,
          overlap: i.tags.filter((t) => selectedTagIds.has(t.tag.id)).length,
        }))
        .sort((a, b) => a.overlap - b.overlap)
        .map(({ item }) => item);
    }

    setResults(candidates.slice(0, 6));
    setStep("results");
  }

  if (step === "results") {
    const msg = liked
      ? same
        ? `${selected?.display_name}처럼 비슷한 스타일이에요`
        : `${selected?.display_name}과 다른 새로운 스타일이에요`
      : same
      ? `${selected?.display_name}처럼 별로일 수 있는 건 빼고요`
      : `${selected?.display_name}과는 완전 다른 걸 골랐어요`;

    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => setStep("select")} className="text-muted-foreground">
            ← 다시 고르기
          </button>
          <h1 className="mt-2 text-xl font-bold">이런 건 어때요?</h1>
          <p className="mt-0.5 text-sm text-muted-foreground">{msg}</p>
        </header>
        <main className="flex-1 px-4 py-4">
          {results.length === 0 ? (
            <p className="py-16 text-center text-muted-foreground">추천할 메뉴가 없어요</p>
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

  if (step === "direction") {
    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => setStep("pref")} className="text-muted-foreground">
            ← 이전
          </button>
          <h1 className="mt-2 text-xl font-bold">
            {liked ? "비슷한 걸 마실까요?" : "그럼 반대 방향으로 가볼까요?"}
          </h1>
        </header>
        <main className="flex flex-1 flex-col gap-3 px-4 py-6">
          <button
            onClick={() => handleDirection(true)}
            className="rounded-xl border border-border bg-card px-5 py-5 text-left hover:border-primary/50"
          >
            <p className="font-semibold">{liked ? "비슷한 스타일" : "그래도 비슷한 걸로"}</p>
            <p className="mt-1 text-sm text-muted-foreground">
              {liked
                ? `${selected?.display_name}과 결이 맞는 것들이에요`
                : "비슷하지만 조금 더 나을 수 있어요"}
            </p>
          </button>
          <button
            onClick={() => handleDirection(false)}
            className="rounded-xl border border-border bg-card px-5 py-5 text-left hover:border-primary/50"
          >
            <p className="font-semibold">{liked ? "전혀 다른 스타일" : "완전히 다른 걸로"}</p>
            <p className="mt-1 text-sm text-muted-foreground">
              {liked
                ? "새로운 세계를 탐험해봐요"
                : `${selected?.display_name}과는 반대 방향이에요`}
            </p>
          </button>
        </main>
      </div>
    );
  }

  if (step === "pref") {
    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => setStep("select")} className="text-muted-foreground">
            ← 이전
          </button>
          <h1 className="mt-2 text-xl font-bold">
            &quot;{selected?.display_name}&quot; 어떠셨어요?
          </h1>
        </header>
        <main className="flex flex-1 flex-col gap-3 px-4 py-6">
          <button
            onClick={() => handlePref(true)}
            className="rounded-xl border border-border bg-card px-5 py-5 text-left hover:border-primary/50"
          >
            <p className="font-semibold">좋았어요 😊</p>
            <p className="mt-1 text-sm text-muted-foreground">비슷하거나 더 나은 걸 찾아드릴게요</p>
          </button>
          <button
            onClick={() => handlePref(false)}
            className="rounded-xl border border-border bg-card px-5 py-5 text-left hover:border-primary/50"
          >
            <p className="font-semibold">별로였어요 😕</p>
            <p className="mt-1 text-sm text-muted-foreground">다른 방향으로 추천드릴게요</p>
          </button>
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
        <h1 className="mt-2 text-xl font-bold">마셔본 것 중에서 골라주세요</h1>
        <p className="text-sm text-muted-foreground">기준점이 될 술을 하나 고르면 돼요</p>
      </header>
      <main className="flex-1 px-4 py-4">
        {loading ? (
          <p className="py-16 text-center text-muted-foreground">불러오는 중...</p>
        ) : allItems.length === 0 ? (
          <p className="py-16 text-center text-muted-foreground">메뉴가 없어요</p>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {allItems.map((item) => (
              <MenuCard key={item.id} item={item} onClick={() => handleSelect(item)} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
