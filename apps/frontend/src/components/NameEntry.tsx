"use client";

import { useState } from "react";
import { setGuestName } from "@/lib/session";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Props {
  onConfirm: (name: string) => void;
}

export default function NameEntry({ onConfirm }: Props) {
  const [value, setValue] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    setGuestName(trimmed);
    onConfirm(trimmed);
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-6">
      <div className="w-full max-w-sm space-y-8 text-center">
        <div className="space-y-2">
          <p className="text-4xl">🥃</p>
          <h1 className="text-2xl font-semibold tracking-tight">hon_bar</h1>
          <p className="text-muted-foreground text-sm">
            오늘 바에 오신 분 이름이 어떻게 되세요?
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="이름을 입력하세요"
            className="h-12 text-center text-base bg-card border-border"
            autoFocus
            maxLength={20}
          />
          <Button
            type="submit"
            className="w-full h-12 text-base bg-primary text-primary-foreground"
            disabled={!value.trim()}
          >
            입장하기
          </Button>
        </form>
      </div>
    </div>
  );
}
