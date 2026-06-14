import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { format, formatDistanceToNow } from "date-fns";

/**
 * Utility to merge tailwind classes safely
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format a date to string (e.g., "Oct 24, 2024")
 */
export function formatDate(date: string | Date | undefined): string {
  if (!date) return "";
  const d = new Date(date);
  return format(d, "MMM d, yyyy");
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
export function formatRelative(date: string | Date | undefined): string {
  if (!date) return "";
  const d = new Date(date);
  return formatDistanceToNow(d, { addSuffix: true });
}

/**
 * Format numbers as currency
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

/**
 * Format numbers with K/M suffixes
 */
export function formatCompactNumber(num: number): string {
  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    compactDisplay: "short",
  }).format(num);
}
