"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { adminApi, getAdminToken } from "@/lib/api";
import type { Order, OrderStatus } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

const STATUS_LABELS: Record<OrderStatus, string> = {
  requested: "요청",
  preparing: "준비 중",
  served: "서빙 완료",
  canceled: "취소",
};

const STATUS_NEXT: Partial<Record<OrderStatus, OrderStatus>> = {
  requested: "preparing",
  preparing: "served",
};

const STATUS_COLORS: Record<OrderStatus, string> = {
  requested: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  preparing: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  served: "bg-green-500/20 text-green-400 border-green-500/30",
  canceled: "bg-muted text-muted-foreground border-border",
};

export default function AdminOrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [updating, setUpdating] = useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      const data = await adminApi.listOrders();
      setOrders(data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()));
    } catch {
      router.replace("/admin/login");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    if (!getAdminToken()) {
      router.replace("/admin/login");
      return;
    }
    fetchOrders();
  }, [fetchOrders, router]);

  async function handleNextStatus(order: Order) {
    const next = STATUS_NEXT[order.status];
    if (!next) return;
    setUpdating(order.id);
    try {
      const updated = await adminApi.updateOrderStatus(order.id, next);
      setOrders((prev) => prev.map((o) => (o.id === updated.id ? updated : o)));
    } catch {
      /* silent */
    } finally {
      setUpdating(null);
    }
  }

  async function handleCancel(order: Order) {
    setUpdating(order.id);
    try {
      const updated = await adminApi.updateOrderStatus(order.id, "canceled");
      setOrders((prev) => prev.map((o) => (o.id === updated.id ? updated : o)));
    } catch {
      /* silent */
    } finally {
      setUpdating(null);
    }
  }

  function formatTime(iso: string) {
    return new Date(iso).toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-muted-foreground">
        불러오는 중...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-10 border-b border-border bg-background/95 px-6 py-4 backdrop-blur">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">주문 관리</h1>
          <Button variant="outline" size="sm" onClick={fetchOrders}>
            새로고침
          </Button>
        </div>
      </header>

      <main className="mx-auto max-w-2xl space-y-3 px-4 py-4">
        {orders.length === 0 ? (
          <p className="py-16 text-center text-muted-foreground">주문이 없어요</p>
        ) : (
          orders.map((order) => {
            const isExpanded = expandedId === order.id;
            const nextStatus = STATUS_NEXT[order.status];
            const isUpdating = updating === order.id;

            return (
              <div
                key={order.id}
                className="overflow-hidden rounded-xl border border-border bg-card"
              >
                {/* Order header */}
                <button
                  className="flex w-full items-center justify-between px-4 py-3 text-left"
                  onClick={() => setExpandedId(isExpanded ? null : order.id)}
                >
                  <div className="flex items-center gap-3">
                    <span className="font-semibold">{order.guest_name}</span>
                    <span className="text-xs text-muted-foreground">{formatTime(order.created_at)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`rounded-full border px-2.5 py-0.5 text-xs font-medium ${STATUS_COLORS[order.status]}`}
                    >
                      {STATUS_LABELS[order.status]}
                    </span>
                    <span className="text-muted-foreground">{isExpanded ? "▲" : "▼"}</span>
                  </div>
                </button>

                {/* Expanded details */}
                {isExpanded && (
                  <div className="border-t border-border">
                    {/* Items list */}
                    <div className="space-y-3 px-4 py-3">
                      {order.order_items.map((oi) => (
                        <div key={oi.id}>
                          <p className="font-medium">{oi.menu_item.display_name}</p>

                          {/* Recipe steps if cocktail */}
                          {oi.menu_item.cocktail?.steps && oi.menu_item.cocktail.steps.length > 0 && (
                            <ol className="mt-2 space-y-1 rounded-lg bg-muted/40 px-3 py-2">
                              {oi.menu_item.cocktail.steps.map((step, i) => (
                                <li key={step.id} className="flex gap-2 text-sm text-muted-foreground">
                                  <span className="shrink-0 font-mono text-primary/70">
                                    {String(i + 1).padStart(2, "0")}
                                  </span>
                                  <span>
                                    {step.item && (
                                      <span className="font-medium text-foreground">{step.item.name} </span>
                                    )}
                                    {step.amount && step.unit && (
                                      <span className="text-primary/80">{step.amount}{step.unit} — </span>
                                    )}
                                    {step.instruction}
                                  </span>
                                </li>
                              ))}
                            </ol>
                          )}

                          {oi.memo && (
                            <p className="mt-1 text-sm text-muted-foreground">메모: {oi.memo}</p>
                          )}
                        </div>
                      ))}
                    </div>

                    {order.memo && (
                      <>
                        <Separator />
                        <p className="px-4 py-2 text-sm text-muted-foreground">주문 메모: {order.memo}</p>
                      </>
                    )}

                    {/* Action buttons */}
                    {order.status !== "served" && order.status !== "canceled" && (
                      <>
                        <Separator />
                        <div className="flex gap-2 px-4 py-3">
                          {nextStatus && (
                            <Button
                              size="sm"
                              disabled={isUpdating}
                              onClick={() => handleNextStatus(order)}
                            >
                              {isUpdating ? "처리 중..." : nextStatus === "preparing" ? "준비 시작" : "서빙 완료"}
                            </Button>
                          )}
                          <Button
                            size="sm"
                            variant="outline"
                            disabled={isUpdating}
                            onClick={() => handleCancel(order)}
                          >
                            취소
                          </Button>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </main>
    </div>
  );
}
