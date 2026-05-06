export function LoadingState({ label = "Loading" }: { label?: string }) {
  return (
    <div className="flex min-h-32 items-center justify-center rounded border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-600">
      {label}
    </div>
  );
}
