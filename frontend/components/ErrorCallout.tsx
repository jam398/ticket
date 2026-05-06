import { AlertTriangle } from "lucide-react";

export function ErrorCallout({ message }: { message: string }) {
  return (
    <div className="flex items-start gap-2 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
      <AlertTriangle className="mt-0.5 h-4 w-4 flex-none" aria-hidden="true" />
      <span>{message}</span>
    </div>
  );
}
