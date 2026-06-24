export type StockStatus = "available" | "low" | "empty" | "unknown";
export type AlcoholLevel = "low" | "medium" | "high";
export type Technique = "build" | "shake" | "stir" | "blend";
export type GlassType = "highball" | "coupe" | "rocks" | "martini" | "shot" | "wine" | "etc";
export type OrderStatus = "requested" | "preparing" | "served" | "canceled";

export interface ItemType {
  id: string;
  name: string;
  display_order: number;
  is_visible: boolean;
  is_active: boolean;
}

export interface Item {
  id: string;
  name: string;
  item_type_id: string;
  item_type: ItemType;
  stock_status: StockStatus;
  abv: number | null;
  memo: string | null;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: string;
  category: string;
  name: string;
  display_name: string;
}

export interface CocktailStep {
  id: string;
  step_order: number;
  instruction: string;
  item_id: string | null;
  item: { id: string; name: string } | null;
  amount: number | null;
  unit: string | null;
  is_required: boolean;
}

export interface Cocktail {
  id: string;
  name: string;
  technique: Technique;
  glass_type: GlassType;
  alcohol_level: AlcoholLevel;
  taste_sweetness: number;
  taste_sourness: number;
  taste_bitterness: number;
  taste_body: number;
  taste_freshness: number;
  is_active: boolean;
  steps: CocktailStep[];
  created_at: string;
  updated_at: string;
}

export interface MenuItemTag {
  tag: Tag;
}

export interface MenuItem {
  id: string;
  display_name: string;
  short_description: string | null;
  image_url: string | null;
  full_description: string | null;
  cocktail_id: string | null;
  item_id: string | null;
  is_active: boolean;
  display_order: number;
  cocktail: Cocktail | null;
  item: Item | null;
  tags: MenuItemTag[];
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: string;
  menu_item_id: string;
  menu_item: MenuItem;
  memo: string | null;
}

export interface Order {
  id: string;
  guest_name: string;
  status: OrderStatus;
  memo: string | null;
  order_items: OrderItem[];
  created_at: string;
}

export interface Review {
  id: string;
  menu_item_id: string;
  guest_name: string;
  rating: number;
  content: string | null;
  created_at: string;
}

export interface RecommendRequest {
  sweetness?: number;
  sourness?: number;
  bitterness?: number;
  alcohol_level?: AlcoholLevel;
  base_item_type_id?: string;
}
