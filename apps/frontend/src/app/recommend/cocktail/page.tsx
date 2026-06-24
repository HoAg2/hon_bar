"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { publicApi } from "@/lib/api";
import { getGuestName } from "@/lib/session";
import type { AlcoholLevel, Cocktail } from "@/types";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

type Step = "taste" | "abv" | "results";

const TASTE_OPTIONS = [
  { label: "달콤한", key: "sweetness" },
  { label: "시큼한", key: "sourness" },
  { label: "씁쓸한", key: "bitterness" },
  { label: "묵직한", key: "body" },
  { label: "청량한", key: "freshness" },
] as const;

const ABV_OPTIONS: { label: string; desc: string; value: AlcoholLevel }[] = [
  { label: "약하게", desc: "~15%", value: "low" },
  { label: "적당히", desc: "15–25%", value: "medium" },
  { label: "강하게", desc: "25%+", value: "high" },
];

const ALCOHOL_LABEL: Record<AlcoholLevel, string> = {
  low: "저도수",
  medium: "중도수",
  high: "고도수",
};

export default function CocktailRecommendPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("taste");
  const [selectedTastes, setSelectedTastes] = useState<Set<string>>(new Set());
  const [abv, setAbv] = useState<AlcoholLevel | null>(null);
  const [results, setResults] = useState<Cocktail[]>([]);
  const [loading, setLoading] = useState(false);

  function toggleTaste(key: string) {
    setSelectedTastes((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  async function handleSubmit() {
    if (!abv) return;
    setLoading(true);
    const body: Record<string, unknown> = { alcohol_level: abv };
    if (selectedTastes.has("sweetness")) body.sweetness = 4;
    if (selectedTastes.has("sourness")) body.sourness = 4;
    if (selectedTastes.has("bitterness")) body.bitterness = 4;
    try {
      const data = await publicApi.recommendCocktails(
        body as Parameters<typeof publicApi.recommendCocktails>[0]
      );
      setResults(data);
      setStep("results");
    } catch {
      /* silent */
    } finally {
      setLoading(false);
    }
  }

  const guestName = getGuestName() ?? "게스트";

  if (step === "results") {
    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => router.back()} className="text-muted-foreground">
            ← 홈으로
          </button>
          <h1 className="mt-2 text-xl font-bold">{guestName}님께 추천드려요</h1>
        </header>
        <main className="flex-1 space-y-3 px-4 py-4">
          {results.length === 0 ? (
            <p className="py-16 text-center text-muted-foreground">
              조건에 맞는 칵테일이 없어요
            </p>
          ) : (
            results.map((c) => (
              <div
                key={c.id}
                className="space-y-2 rounded-xl border border-border bg-card p-4"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="font-semibold">{c.name}</p>
                  <Badge>{ALCOHOL_LABEL[c.alcohol_level]}</Badge>
                </div>
                <div className="flex flex-wrap gap-2">
                  {[
                    { label: "단맛", v: c.taste_sweetness },
                    { label: "신맛", v: c.taste_sourness },
                    { label: "쓴맛", v: c.taste_bitterness },
                  ].map(({ label, v }) => (
                    <div key={label} className="flex items-center gap-1 text-xs text-muted-foreground">
                      <span>{label}</span>
                      <div className="flex gap-0.5">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <div
                            key={i}
                            className={`h-1.5 w-3 rounded-sm ${i < v ? "bg-primary" : "bg-border"}`}
                          />
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </main>
        <div className="border-t border-border px-4 py-4">
          <Button variant="outline" className="w-full" onClick={() => setStep("taste")}>
            다시 추천받기
          </Button>
        </div>
      </div>
    );
  }

  if (step === "abv") {
    return (
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <header className="border-b border-border px-4 py-4">
          <button onClick={() => setStep("taste")} className="text-muted-foreground">
            ← 이전
          </button>
          <h1 className="mt-2 text-xl font-bold">도수는 어느 정도가 좋으세요?</h1>
        </header>
        <main className="flex flex-1 flex-col gap-3 px-4 py-6">
          {ABV_OPTIONS.map((o) => (
            <button
              key={o.value}
              onClick={() => setAbv(o.value)}
              className={`rounded-xl border px-5 py-4 text-left transition-colors ${
                abv === o.value
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-card text-foreground hover:border-primary/50"
              }`}
            >
              <span className="font-semibold">{o.label}</span>
              <span className="ml-2 text-sm text-muted-foreground">({o.desc})</span>
            </button>
          ))}
        </main>
        <div className="border-t border-border px-4 py-4">
          <Button
            className="w-full"
            size="lg"
            disabled={!abv || loading}
            onClick={handleSubmit}
          >
            {loading ? "추천 중..." : "추천받기"}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <header className="border-b border-border px-4 py-4">
        <button onClick={() => router.back()} className="text-muted-foreground">
          ← 홈으로
        </button>
        <h1 className="mt-2 text-xl font-bold">어떤 맛이 끌리세요?</h1>
        <p className="text-sm text-muted-foreground">여러 개 골라도 돼요</p>
      </header>
      <main className="flex flex-1 flex-wrap content-start gap-3 px-4 py-6">
        {TASTE_OPTIONS.map((o) => (
          <button key={o.key} onClick={() => toggleTaste(o.key)}>
            <Badge
              variant={selectedTastes.has(o.key) ? "default" : "outline"}
              className="cursor-pointer px-4 py-2 text-base"
            >
              {o.label}
            </Badge>
          </button>
        ))}
      </main>
      <div className="border-t border-border px-4 py-4">
        <Button className="w-full" size="lg" onClick={() => setStep("abv")}>
          다음
        </Button>
      </div>
    </div>
  );
}
