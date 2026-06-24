"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

interface Props {
  guestName: string;
  onChangeName: () => void;
}

export default function MainScreen({ guestName, onChangeName }: Props) {
  return (
    <div className="flex min-h-screen flex-col px-4 pb-8">
      {/* header */}
      <header className="flex items-center justify-between py-5">
        <span className="text-lg font-semibold tracking-tight">🥃 hon_bar</span>
        <button
          onClick={onChangeName}
          className="text-xs text-muted-foreground underline underline-offset-2"
        >
          {guestName}님
        </button>
      </header>

      {/* welcome */}
      <div className="mt-4 mb-8">
        <h2 className="text-xl font-medium leading-snug">
          {guestName}님, 오늘은<br />
          <span className="text-primary">어떤 한 잔</span>을 마셔볼까요?
        </h2>
      </div>

      {/* CTA buttons */}
      <div className="space-y-3 mb-10">
        <Link href="/recommend/cocktail" className="block">
          <Button
            variant="outline"
            className="w-full h-16 text-base justify-start gap-4 border-border bg-card hover:bg-accent"
          >
            <span className="text-2xl">🍹</span>
            <div className="text-left">
              <p className="font-medium">칵테일 추천받기</p>
              <p className="text-xs text-muted-foreground font-normal">취향에 맞는 칵테일 찾기</p>
            </div>
          </Button>
        </Link>

        <Link href="/recommend/whisky" className="block">
          <Button
            variant="outline"
            className="w-full h-16 text-base justify-start gap-4 border-border bg-card hover:bg-accent"
          >
            <span className="text-2xl">🥃</span>
            <div className="text-left">
              <p className="font-medium">위스키 추천받기</p>
              <p className="text-xs text-muted-foreground font-normal">마셔본 위스키 기반 추천</p>
            </div>
          </Button>
        </Link>

        <Link href="/recommend/whisky-beginner" className="block">
          <Button
            variant="outline"
            className="w-full h-16 text-base justify-start gap-4 border-border bg-card hover:bg-accent"
          >
            <span className="text-2xl">🌱</span>
            <div className="text-left">
              <p className="font-medium">위스키가 처음이에요</p>
              <p className="text-xs text-muted-foreground font-normal">향으로 골라보는 입문 위스키</p>
            </div>
          </Button>
        </Link>
      </div>

      {/* divider */}
      <p className="text-xs text-muted-foreground mb-4 tracking-widest uppercase">전체 메뉴</p>

      {/* placeholder — menu list will be added next */}
      <div className="flex-1 flex items-center justify-center">
        <p className="text-muted-foreground text-sm">메뉴 목록 준비 중</p>
      </div>
    </div>
  );
}
