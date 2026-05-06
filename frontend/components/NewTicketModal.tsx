import { X } from "lucide-react";
import { FormEvent, useState } from "react";
import { SOURCE_OPTIONS } from "@/lib/constants";
import type { NewTicketPayload, TicketSource } from "@/lib/types";

const initialForm: NewTicketPayload = {
  title: "",
  description: "",
  customer_name: "",
  customer_email: "",
  source: "web_form",
  tags: [],
};

export function NewTicketModal({
  open,
  saving,
  onClose,
  onSubmit,
}: {
  open: boolean;
  saving: boolean;
  onClose: () => void;
  onSubmit: (payload: NewTicketPayload) => Promise<void>;
}) {
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState<string | null>(null);

  if (!open) {
    return null;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (!form.title.trim() || !form.description.trim() || !form.customer_name.trim() || !form.customer_email.trim()) {
      setError("Title, description, customer name, and customer email are required.");
      return;
    }
    await onSubmit({
      ...form,
      tags: form.tags.filter(Boolean),
    });
    setForm(initialForm);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/35 p-4">
      <div
        className="w-full max-w-2xl rounded border border-slate-200 bg-white shadow-soft"
        role="dialog"
        aria-modal="true"
        aria-label="New Ticket"
      >
        <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
          <h2 className="text-base font-semibold text-slate-950">New Ticket</h2>
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
            <span className="text-sm font-medium text-slate-700">Title</span>
            <input
              value={form.title}
              onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
              className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Description</span>
            <textarea
              value={form.description}
              onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
              className="mt-1 min-h-28 w-full rounded border border-slate-300 px-3 py-2 text-sm"
            />
          </label>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Customer Name</span>
              <input
                value={form.customer_name}
                onChange={(event) => setForm((current) => ({ ...current, customer_name: event.target.value }))}
                className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Customer Email</span>
              <input
                value={form.customer_email}
                onChange={(event) => setForm((current) => ({ ...current, customer_email: event.target.value }))}
                className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm"
              />
            </label>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Source</span>
              <select
                value={form.source}
                onChange={(event) =>
                  setForm((current) => ({ ...current, source: event.target.value as TicketSource }))
                }
                className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm"
              >
                {SOURCE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Tags optional</span>
              <input
                value={form.tags.join(", ")}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    tags: event.target.value.split(",").map((tag) => tag.trim()),
                  }))
                }
                className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm"
                placeholder="login, billing"
              />
            </label>
          </div>
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
              className="rounded bg-slate-900 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-500"
            >
              {saving ? "Creating" : "Create Ticket"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
