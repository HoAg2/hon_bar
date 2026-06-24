import type {
  MenuItem,
  Cocktail,
  Tag,
  Order,
  Review,
  RecommendRequest,
} from "@/types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

// ─── Public ──────────────────────────────────────────────

export const publicApi = {
  listMenu: (params?: { tag_id?: string; search?: string }) => {
    const qs = new URLSearchParams();
    if (params?.tag_id) qs.set("tag_id", params.tag_id);
    if (params?.search) qs.set("search", params.search);
    const q = qs.toString();
    return request<MenuItem[]>(`/menu${q ? `?${q}` : ""}`);
  },

  getMenuItem: (id: string) => request<MenuItem>(`/menu/${id}`),

  getAvailableCocktails: () => request<Cocktail[]>("/cocktails/available"),

  recommendCocktails: (body: RecommendRequest) =>
    request<Cocktail[]>("/cocktails/recommend", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  createOrder: (body: {
    guest_name: string;
    memo?: string;
    items: { menu_item_id: string; memo?: string }[];
  }) =>
    request<Order>("/orders", { method: "POST", body: JSON.stringify(body) }),

  listReviews: (menu_item_id?: string) => {
    const q = menu_item_id ? `?menu_item_id=${menu_item_id}` : "";
    return request<Review[]>(`/reviews${q}`);
  },

  createReview: (body: {
    menu_item_id: string;
    guest_name: string;
    rating: number;
    content?: string;
  }) =>
    request<Review>("/reviews", { method: "POST", body: JSON.stringify(body) }),
};

// ─── Admin ───────────────────────────────────────────────

let _token: string | null = null;

export function setAdminToken(token: string) {
  _token = token;
  if (typeof window !== "undefined") {
    sessionStorage.setItem("hon_bar_admin_token", token);
  }
}

export function getAdminToken(): string | null {
  if (_token) return _token;
  if (typeof window !== "undefined") {
    _token = sessionStorage.getItem("hon_bar_admin_token");
  }
  return _token;
}

function adminRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAdminToken();
  return request<T>(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers ?? {}),
    },
  });
}

export const adminApi = {
  login: (password: string) =>
    request<{ access_token: string; token_type: string }>("/admin/login", {
      method: "POST",
      body: JSON.stringify({ password }),
    }),

  listTags: (category?: string) => {
    const q = category ? `?category=${category}` : "";
    return adminRequest<Tag[]>(`/admin/tags${q}`);
  },

  listOrders: (status?: string) => {
    const q = status ? `?status=${status}` : "";
    return adminRequest<Order[]>(`/admin/orders${q}`);
  },

  getOrder: (id: string) => adminRequest<Order>(`/admin/orders/${id}`),

  updateOrderStatus: (id: string, status: string) =>
    adminRequest<Order>(`/admin/orders/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
};
