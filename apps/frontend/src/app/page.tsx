"use client";

import { useEffect, useState } from "react";
import { getGuestName, setGuestName } from "@/lib/session";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import NameEntry from "@/components/NameEntry";
import MainScreen from "@/components/MainScreen";

export default function Home() {
  const [name, setName] = useState<string | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setName(getGuestName());
    setReady(true);
  }, []);

  if (!ready) return null;

  if (!name) {
    return <NameEntry onConfirm={(n) => setName(n)} />;
  }

  return <MainScreen guestName={name} onChangeName={() => setName(null)} />;
}
