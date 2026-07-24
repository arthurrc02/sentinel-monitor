interface HeaderProps {
  title: string;
  onToggleNav: () => void;
  isRefreshing?: boolean;
}

export function Header({ title, onToggleNav, isRefreshing = false }: HeaderProps) {
  return (
    <header className="flex items-center gap-3 border-b border-slate-200 bg-white px-4 py-3 md:px-6">
      <button
        type="button"
        onClick={onToggleNav}
        className="rounded-md p-2 text-slate-600 transition-colors hover:bg-slate-100 md:hidden"
        aria-label="Abrir menu de navegação"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          className="h-5 w-5"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5"
          />
        </svg>
      </button>
      <h1 className="text-base font-semibold text-slate-900">{title}</h1>
      {isRefreshing && (
        <span className="text-xs text-slate-400" role="status">
          Atualizando...
        </span>
      )}
    </header>
  );
}
