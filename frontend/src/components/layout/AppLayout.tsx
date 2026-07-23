import { useState, type ReactNode } from "react";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

interface AppLayoutProps {
  title: string;
  children: ReactNode;
  isRefreshing?: boolean;
}

export function AppLayout({ title, children, isRefreshing = false }: AppLayoutProps) {
  const [isNavOpen, setIsNavOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar isOpen={isNavOpen} onClose={() => setIsNavOpen(false)} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header
          title={title}
          onToggleNav={() => setIsNavOpen((open) => !open)}
          isRefreshing={isRefreshing}
        />
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
