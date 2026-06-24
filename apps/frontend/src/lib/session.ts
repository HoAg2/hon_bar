const KEY = "hon_bar_guest_name";

export function getGuestName(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(KEY);
}

export function setGuestName(name: string): void {
  localStorage.setItem(KEY, name.trim());
}

export function clearGuestName(): void {
  localStorage.removeItem(KEY);
}
