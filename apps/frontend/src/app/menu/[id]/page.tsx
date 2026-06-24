"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { publicApi } from "@/lib/api";
import { getGuestName } from "@/lib/session";
import type { MenuItem } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

const ALCOHOL_LABEL: Record<string, string> = {
  low: "저도수",
  medium: "중도수",
  high: "고도수",
};

const TECHNIQUE_LABEL: Record<string, string> = {
  build: "빌드",
  shake: "쉐이크",
  stir: "스터",
  blend: "블렌드",
};

export default function MenuDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [item, setItem] = useState<MenuItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [ordering, setOrdering] = useState(false);
  const [ordered, setOrdered] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    publicApi
      .getMenuItem(id)
      .then(setItem)
      .catch(() => setError("메뉴를 불러올 수 없어요"))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleOrder() {
    if (!item) return;
    const name = getGuestName();
    if (!name) {
      router.push("/");
      return;
    }
    setOrdering(true);
    try {
      await publicApi.createOrder({
        guest_name: name,
        items: [{ menu_item_id: item.id }],
      });
      setOrdered(true);
    } catch {
      setError("주문에 실패했어요. 다시 시도해 주세요.");
    } finally {
      setOrdering(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-muted-foreground">
        불러오는 중...
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 px-4">
        <p className="text-muted-foreground">{error ?? "메뉴를 찾을 수 없어요"}</p>
        <Button variant="outline" onClick={() => router.back()}>돌아가기</Button>
      </div>
    );
  }

  const cocktail = item.cocktail;

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      {/* Back */}
      <header className="sticky top-0 z-10 border-b border-border bg-background/95 px-4 py-3 backdrop-blur">
        <button
          onClick={() => router.back()}
          className="text-muted-foreground hover:text-foreground"
        >
          ← 메뉴로
        </button>
      </header>

      <main className="flex-1 pb-28">
        {/* Image */}
        <div className="aspect-video w-full overflow-hidden bg-muted">
          {item.image_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={item.image_url}
              alt={item.display_name}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-6xl">🍹</div>
          )}
        </div>

        <div className="px-4 py-5 space-y-4">
          {/* Title + Tags */}
          <div>
            <h1 className="text-2xl font-bold">{item.display_name}</h1>
            {item.tags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {item.tags.map(({ tag }) => (
                  <Badge key={tag.id} variant="outline">{tag.display_name}</Badge>
                ))}
              </div>
            )}
          </div>

          {/* Description */}
          {item.short_description && (
            <p className="text-muted-foreground">{item.short_description}</p>
          )}

          {/* Cocktail details */}
          {cocktail && (
            <>
              <Separator />
              <div className="space-y-2">
                <div className="flex gap-2 flex-wrap">
                  <Badge>{ALCOHOL_LABEL[cocktail.alcohol_level] ?? cocktail.alcohol_level}</Badge>
                  <Badge variant="outline">{TECHNIQUE_LABEL[cocktail.technique] ?? cocktail.technique}</Badge>
                </div>

                {/* Taste bars */}
                <div className="space-y-1.5">
                  {[
                    { label: "단맛", v: cocktail.taste_sweetness },
                    { label: "신맛", v: cocktail.taste_sourness },
                    { label: "쓴맛", v: cocktail.taste_bitterness },
                    { label: "바디", v: cocktail.taste_body },
                    { label: "청량감", v: cocktail.taste_freshness },
                  ].map(({ label, v }) => (
                    <div key={label} className="flex items-center gap-2 text-sm">
                      <span className="w-14 shrink-0 text-muted-foreground">{label}</span>
                      <div className="flex gap-0.5">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <div
                            key={i}
                            className={`h-2 w-5 rounded-sm ${i < v ? "bg-primary" : "bg-border"}`}
                          />
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Steps */}
              {cocktail.steps.length > 0 && (
                <>
                  <Separator />
                  <div className="space-y-2">
                    <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">레시피</p>
                    <ol className="space-y-2">
                      {cocktail.steps.map((step, i) => (
                        <li key={step.id} className="flex gap-3 text-sm">
                          <span className="shrink-0 font-mono text-primary">{String(i + 1).padStart(2, "0")}</span>
                          <span className="text-muted-foreground">
                            {step.item && (
                              <span className="font-medium text-foreground">{step.item.name} </span>
                            )}
                            {step.amount && step.unit && (
                              <span className="text-primary">{step.amount}{step.unit} — </span>
                            )}
                            {step.instruction}
                          </span>
                        </li>
                      ))}
                    </ol>
                  </div>
                </>
              )}
            </>
          )}

          {/* Full description */}
          {item.full_description && (
            <>
              <Separator />
              <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                {item.full_description}
              </p>
            </>
          )}
        </div>
      </main>

      {/* Fixed order button */}
      <div className="fixed bottom-0 left-0 right-0 border-t border-border bg-background/95 px-4 py-4 backdrop-blur">
        {ordered ? (
          <div className="rounded-lg bg-card border border-primary/30 px-4 py-3 text-center text-primary font-medium">
            주문이 접수됐어요 🥂
          </div>
        ) : (
          <Button
            className="w-full"
            size="lg"
            onClick={handleOrder}
            disabled={ordering}
          >
            {ordering ? "주문 중..." : "주문하기"}
          </Button>
        )}
        {error && <p className="mt-2 text-center text-xs text-destructive">{error}</p>}
      </div>
    </div>
  );
}
