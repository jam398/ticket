"use client";

import Link from "next/link";
import { ArrowLeft, CheckCircle2, Send } from "lucide-react";
import { FormEvent, useState } from "react";
import { createTicket } from "@/lib/api";
import type { NewTicketPayload } from "@/lib/types";

const initialForm: NewTicketPayload = {
  title: "",
  description: "",
  customer_name: "",
  customer_email: "",
  source: "web_form",
  tags: ["employee-submitted"],
};

export default function CreateTicketPage() {
  const [form, setForm] = useState(initialForm);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createdTicketId, setCreatedTicketId] = useState<number | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setCreatedTicketId(null);

    if (!form.title.trim() || !form.description.trim() || !form.customer_name.trim() || !form.customer_email.trim()) {
      setError("Title, description, name, and email are required.");
      return;
    }

    setSaving(true);
    try {
      const created = await createTicket({
        ...form,
        title: form.title.trim(),
        description: form.description.trim(),
        customer_name: form.customer_name.trim(),
        customer_email: form.customer_email.trim(),
        tags: form.tags.filter(Boolean),
      });
      setCreatedTicketId(created.id);
      setForm(initialForm);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to create ticket.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="min-h-screen bg-white px-4 py-8">
      <div className="mx-auto max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center gap-2 rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Back
        </Link>

        <section className="mt-6 rounded border border-slate-200 bg-white shadow-soft">
          <div className="border-b border-slate-200 px-5 py-4">
            <p className="text-sm font-medium uppercase tracking-normal text-blue-700">Employee request</p>
            <h1 className="mt-1 text-2xl font-semibold tracking-normal text-slate-950">Create Ticket</h1>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Submit the issue details so IT can review, triage, and resolve the request.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 p-5">
            {createdTicketId ? (
              <div className="flex items-start gap-2 rounded border border-green-200 bg-green-50 p-3 text-sm text-green-800">
                <CheckCircle2 className="mt-0.5 h-4 w-4 flex-none" aria-hidden="true" />
                <span>Ticket #{createdTicketId} was created.</span>
              </div>
            ) : null}

            {error ? <p className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">{error}</p> : null}

            <label className="block">
              <span className="text-sm font-medium text-slate-700">Issue title</span>
              <input
                value={form.title}
                onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
                className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm text-slate-900"
                placeholder="Dashboard not loading"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700">Description</span>
              <textarea
                value={form.description}
                onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
                className="mt-1 min-h-32 w-full rounded border border-slate-300 px-3 py-2 text-sm text-slate-900"
                placeholder="Describe what happened, what you expected, and any error message you saw."
              />
            </label>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Your name</span>
                <input
                  value={form.customer_name}
                  onChange={(event) => setForm((current) => ({ ...current, customer_name: event.target.value }))}
                  className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm text-slate-900"
                  placeholder="Avery Stone"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-slate-700">Work email</span>
                <input
                  type="email"
                  value={form.customer_email}
                  onChange={(event) => setForm((current) => ({ ...current, customer_email: event.target.value }))}
                  className="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm text-slate-900"
                  placeholder="avery@example.com"
                />
              </label>
            </div>

            <div className="flex flex-col gap-3 border-t border-slate-200 pt-4 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-sm text-slate-500">New tickets start as medium priority until IT reviews them.</p>
              <button
                type="submit"
                disabled={saving}
                className="inline-flex items-center justify-center gap-2 rounded bg-blue-700 px-4 py-2 text-sm font-medium text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-400"
              >
                <Send className="h-4 w-4" aria-hidden="true" />
                {saving ? "Creating" : "Create Ticket"}
              </button>
            </div>
          </form>
        </section>
      </div>
    </main>
  );
}
