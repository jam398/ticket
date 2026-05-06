import { FormEvent, useEffect, useState } from "react";
import { X } from "lucide-react";

export function ResolveTicketModal({
  open,
  saving,
  initialNotes,
  onClose,
  onSubmit,
}: {
  open: boolean;
  saving: boolean;
  initialNotes: string;
  onClose: () => void;
  onSubmit: (notes: string) => Promise<void>;
}) {
  const [notes, setNotes] = useState(initialNotes);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open) {
      setNotes(initialNotes);
      setError(null);
    }
  }, [initialNotes, open]);

  if (!open) {
    return null;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (!notes.trim()) {
      setError("Resolution notes are required.");
      return;
    }
    await onSubmit(notes.trim());
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/35 p-4">
      <div
        className="w-full max-w-xl rounded border border-slate-200 bg-white shadow-soft"
        role="dialog"
        aria-modal="true"
        aria-label="Resolve Ticket"
      >
        <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
          <h2 className="text-base font-semibold text-slate-950">Resolve Ticket</h2>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-8 w-8 items-center justify-center rounded border border-slate-300 text-slate-600 hover:bg-slate-50"
            title="Close"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4 p-4">
          {error ? <p className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">{error}</p> : null}
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Resolution Notes</span>
            <textarea
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              className="mt-1 min-h-36 w-full rounded border border-slate-300 px-3 py-2 text-sm"
            />
          </label>
          <div className="flex justify-end gap-2 border-t border-slate-200 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="rounded border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="rounded bg-blue-700 px-3 py-2 text-sm font-medium text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              {saving ? "Saving" : "Save Resolution"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
